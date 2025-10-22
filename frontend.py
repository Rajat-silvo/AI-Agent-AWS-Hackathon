import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# ---------- CONFIG ----------
API_BASE_URL = "https://8eaiz25hnb.execute-api.us-east-1.amazonaws.com/dev"  # 🔹 Replace with your Lambda’s API Gateway endpoint

# ---------- HELPER FUNCTIONS (Replaced DynamoDB calls with API calls) ----------

def fetch_logs():
    """Fetch cost-saving logs from Lambda backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/fetch-logs")
        if response.status_code == 200:
            data = response.json()
            for item in data:
                item['cost_saved'] = float(item.get('cost_saved', 0))
                item['hours_saved'] = float(item.get('hours_saved', 0))
                item['week_number'] = int(item.get('week_number', 0))
                item['date'] = pd.to_datetime(item.get('date'))
            return pd.DataFrame(data)
        else:
            st.error(f"Failed to fetch logs: {response.text}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return pd.DataFrame()

def fetch_toggle_status():
    """Fetch ON/OFF status from backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/toggle-status")
        if response.status_code == 200:
            return response.json().get("status", "ON").upper() == "ON"
        return True
    except Exception as e:
        st.warning(f"Could not fetch toggle status: {e}")
        return True

def update_toggle_status(new_status):
    """Update ON/OFF toggle status in backend"""
    try:
        payload = {"status": new_status}
        response = requests.post(f"{API_BASE_URL}/update-toggle", json=payload)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to update toggle: {response.text}")
            return False
    except Exception as e:
        st.error(f"Backend error: {e}")
        return False

# ---------- UI LAYOUT ----------
st.set_page_config(page_title="AWS Infra Alarms Dashboard", layout="wide")
st.title("🛠️ AWS Infra Alarms Dashboard")

tab1, tab2 = st.tabs(["📉 EC2 Shutdown (Auto Alarm)", "📝 Manual Alarms"])

# ---------- TAB 1: Auto EC2 Shutdown ----------
with tab1:
    st.subheader("🔌 EC2 Auto-Shutdown Toggle")

    current_status = fetch_toggle_status()
    st.markdown(f"*Current Status:* {'🟢 ON' if current_status else '🔴 OFF'}")

    if st.button("🔁 Toggle EC2 Stop Feature", key="ec2_toggle_button"):
        new_status = "OFF" if current_status else "ON"
        success = update_toggle_status(new_status)
        if success:
            st.success(f"Feature toggled to {new_status}")
            st.session_state['toggle'] = not st.session_state.get('toggle', False)

    st.subheader("📊 Cost-Saving Logs")
    df = fetch_logs()
    if df.empty:
        st.warning("No data available.")
    else:
        selected_date_range = st.date_input("📅 Filter by date", [])
        if len(selected_date_range) == 2:
            start_date = pd.Timestamp(selected_date_range[0]).tz_localize('UTC')
            end_date = pd.Timestamp(selected_date_range[1]).tz_localize('UTC')
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

        with st.expander("📋 View Raw Cost-Saving Logs"):
            st.dataframe(
                df.sort_values(by='date', ascending=False).style.format({
                    'cost_saved': '${:,.2f}',
                    'hours_saved': '{:,.1f}',
                    'week_number': '{:d}',
                    'date': lambda x: x.strftime('%Y-%m-%d %H:%M:%S'),
                })
            )

        weekly = df.groupby('week_number').agg({
            'cost_saved': 'sum',
            'hours_saved': 'sum'
        }).reset_index()

        st.subheader("📈 Weekly Savings")
        st.bar_chart(weekly.set_index('week_number')['cost_saved'])
        st.success(f"✅ Total Savings: *${df['cost_saved'].sum():.2f}*")

# ---------- TAB 2: Manual Alarms ----------
with tab2:
    st.subheader("📋 Manual Security Alarms")

    with st.expander("🔐 MFA for IAM Users"):
        st.markdown("""
        *Alarm:* Multiple IAM users have password login enabled but no MFA configured.
        *Risk:* Users without MFA are more vulnerable to compromised credentials.

        *✅ Resolution Steps:*
        1. Go to [IAM Users Console](https://console.aws.amazon.com/iam/home#/users)
        2. Select a user → Security credentials
        3. Click *Assign MFA device*
        4. Choose *Virtual MFA* (e.g., Google Authenticator)
        5. Complete the MFA setup steps
        """)
        st.button("✅ Mark as Resolved (Manual)", key="resolve_mfa")

    with st.expander("🛡️ CloudTrail Logs Not Encrypted Using KMS CMKs"):
        st.markdown("""
   *Alarm:* CloudTrail logs stored in the S3 bucket are not encrypted using a KMS CMK.
        *Bucket:* ⁠ cloudanix-cloudtrail-logs-522185705600 ⁠
        *Risk:* Logs are encrypted with SSE-S3, not CMK — less secure.

        *✅ Resolution Steps:*
        1. Go to [KMS Console](https://console.aws.amazon.com/kms/home)
        2. Create a *Customer Managed Key (CMK)*
        3. Grant CloudTrail access to the CMK
        4. Open [CloudTrail Console](https://console.aws.amazon.com/cloudtrail)
        5. Edit your trail → Select the CMK under *Log file SSE-KMS Encryption*
        """)
        st.button("✅ Mark as Resolved (Manual)", key="resolve_cloudtrail")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("Created by your automation system — EC2 Shutdown Manager 💼")
