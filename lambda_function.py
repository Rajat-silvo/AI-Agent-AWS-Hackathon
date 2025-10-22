import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

ec2 = boto3.client('ec2')
dynamodb = boto3.resource('dynamodb')

# Tables
log_table = dynamodb.Table('ec2_savings_log')
toggle_table = dynamodb.Table('ec2_toggle')

def get_toggle_status(toggle_name='ec2_stop_feature'):
    try:
        response = toggle_table.get_item(
            Key={'toggle_name': toggle_name}
        )
        if 'Item' in response:
            status = response['Item'].get('status', 'ON')
            print(f"Toggle status: {status}")
            return status.upper()
    except Exception as e:
        print(f"Error fetching toggle status: {str(e)}")
    return 'ON'

def update_toggle_status(status, toggle_name='ec2_stop_feature'):
    try:
        toggle_table.put_item(
            Item={
                'toggle_name': toggle_name,
                'status': status
            }
        )
        print(f"Toggle status updated to {status}")
        return True
    except Exception as e:
        print(f"Failed to update toggle status: {str(e)}")
        return False

def fetch_logs_from_dynamodb():
    """Fetch all logs from DynamoDB"""
    try:
        response = log_table.scan()
        items = response.get('Items', [])
        
        # Convert Decimal to float for JSON serialization
        for item in items:
            if 'cost_saved' in item:
                item['cost_saved'] = float(item['cost_saved'])
            if 'hours_saved' in item:
                item['hours_saved'] = float(item['hours_saved'])
        
        return items
    except Exception as e:
        print(f"Error fetching logs: {str(e)}")
        return []

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))
    
    # CORS headers for all responses
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS request (CORS preflight)
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'OK'})
        }
    
    # Check if this is an API Gateway HTTP API event
    if 'requestContext' in event and 'http' in event['requestContext']:
        http_method = event['requestContext']['http']['method']
        raw_path = event['requestContext']['http']['path']
        
        print(f"HTTP Method: {http_method}, Path: {raw_path}")
        
        # Route: GET /fetch-logs
        if http_method == 'GET' and '/fetch-logs' in raw_path:
            logs = fetch_logs_from_dynamodb()
            clean_logs = convert_decimals(logs)
            return {
                'statusCode': 200,
                'headers': headers,
                #'body': json.dumps(logs)
                'body': json.dumps(clean_logs)

            }
        
        # Route: GET /toggle-status
        elif http_method == 'GET' and '/toggle-status' in raw_path:
            status = get_toggle_status()
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'status': status})
            }
        
        # Route: POST /update-toggle
        elif http_method == 'POST' and '/update-toggle' in raw_path:
            try:
                body = json.loads(event.get('body', '{}'))
                status = body.get('status', '').upper()
                
                if status not in ['ON', 'OFF']:
                    return {
                        'statusCode': 400,
                        'headers': headers,
                        'body': json.dumps({'error': 'Invalid status. Use ON or OFF'})
                    }
                
                success = update_toggle_status(status)
                if success:
                    return {
                        'statusCode': 200,
                        'headers': headers,
                        'body': json.dumps({'message': f'Toggle updated to {status}'})
                    }
                else:
                    return {
                        'statusCode': 500,
                        'headers': headers,
                        'body': json.dumps({'error': 'Failed to update toggle'})
                    }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({'error': str(e)})
                }
        
        # Route not found
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not Found', 'path': raw_path, 'method': http_method})
            }
    
    # Handle SNS event (EC2 auto-shutdown)
    elif 'Records' in event and len(event['Records']) > 0:
        record = event['Records'][0]
        
        if 'Sns' in record:
            # Check if feature is enabled
            if get_toggle_status() != 'ON':
                print("EC2 stop feature is toggled OFF. Skipping instance stop.")
                return {
                    'statusCode': 200,
                    'body': "EC2 stop feature is OFF. No instances stopped."
                }
            
            try:
                message = json.loads(record['Sns']['Message'])
                print("Parsed SNS message:", message)
                
                # Extract instance ID
                instance_id = None
                dimensions = message.get('Trigger', {}).get('Dimensions', [])
                for dim in dimensions:
                    if dim['name'] == 'InstanceId':
                        instance_id = dim['value']
                
                if not instance_id:
                    return {'statusCode': 400, 'body': "No instance ID found"}
                
                print(f"Stopping instance: {instance_id}")
                response = ec2.stop_instances(InstanceIds=[instance_id])
                print(f"Stop response: {response}")
                
                # Log savings
                cost_per_hour = Decimal("0.0104")
                idle_hours = Decimal("12")
                savings = cost_per_hour * idle_hours
                now = datetime.utcnow()
                
                log_table.put_item(
                    Item={
                        'id': str(uuid.uuid4()),
                        'instance_id': instance_id,
                        'date': now.isoformat() + "Z",
                        'week_number': now.isocalendar().week,
                        'hours_saved': idle_hours,
                        'cost_saved': savings
                    }
                )
                
                print(f"✅ Logged to DynamoDB: {instance_id}, savings: ${savings}")
                
                return {
                    'statusCode': 200,
                    'body': f"Successfully stopped instance {instance_id}"
                }
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                return {
                    'statusCode': 500,
                    'body': f"Error: {str(e)}"
                }
    
    # Direct invocation (legacy support)
    elif isinstance(event, dict) and 'status' in event:
        status = event['status'].upper()
        if status in ['ON', 'OFF']:
            success = update_toggle_status(status)
            return {
                'statusCode': 200,
                'body': f'Toggle updated to {status}'
            }
        else:
            return {
                'statusCode': 400,
                'body': 'Invalid status value'
            }
    
    # Unknown event type
    return {
        'statusCode': 400,
        'headers': headers,
        'body': json.dumps({'error': 'Unknown event type', 'event': str(event)})
    }