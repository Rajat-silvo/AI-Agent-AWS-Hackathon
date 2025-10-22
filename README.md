# CloudWise: AI Agents for AWS Cost & Compliance Optimization
Your intelligent AWS co‑pilot for cost and security optimization.

<img width="602" height="285" alt="Dashboard Image1" src="https://github.com/user-attachments/assets/a1efc2fb-6dc7-4936-8696-fbd6a9712476" />
<img width="602" height="241" alt="Dashboard Image2" src="https://github.com/user-attachments/assets/da944654-fbae-4982-a2a2-dd58e075dd5a" />
<img width="602" height="203" alt="Dashboard Image3" src="https://github.com/user-attachments/assets/91dc5496-7275-4eae-807a-1360e8f58ab8" />
<img width="602" height="180" alt="Dashboard Image4" src="https://github.com/user-attachments/assets/745a78f3-e32d-4ea4-a90e-9dbe4ff0025c" />


## Inspiration
Up to 40% of a DevOps engineer’s time is spent silencing or triaging false CloudWatch alarms, often leading to wasted effort, increased costs, and reduced focus on high-value tasks. CloudWise emerged to solve this recurring inefficiency through AI‑driven intelligence that automates monitoring, remediation, and compliance management in AWS environments.

## What It Does
<img width="454" height="681" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/b51d4b2a-7272-4afc-a7dc-c8a087884473" />

CloudWise continuously monitors your AWS environment for:
### Cost inefficiencies: Detects idle EC2 instances and shuts them down.
### Compliance risks: Scans S3 buckets for public exposure.
### Automation: Executes remediation actions via Lambda functions.
### Visualization: Displays savings, compliance status, and AI reasoning through a Streamlit dashboard in real time.
 At its core lies Amazon Bedrock’s Titan Model, which reasons about system events, ranks alerts, and recommends or executes actions like transforming reactive tasks into proactive optimization.

## How We Built It
 Architecture: Modular and serverless.
 Core AWS components:
 Lambda – executes autonomous actions.
 DynamoDB – logs and stores cost/compliance data.
 CloudWatch – monitors metrics and triggers automation.
 Config + PowerPipe – enforces compliance benchmarks.
 AI Reasoning: Amazon Bedrock’s Titan Foundation Model powers decision‑making.
 Visualization: Streamlit dashboard integrated with PowerPipe for live reporting.
 Tech Stack Overview:
  Category
  Tools/Frameworks
  Languages
  Python, Bash
  Frontend
  Streamlit
  Database
  Amazon DynamoDB
  AI Model
  Amazon Bedrock (Titan)
  Automation
  AWS Lambda
  Monitoring
  CloudWatch, PowerPipe
  Deployment
  AWS CLI, boto3 SDK, Bash Scripts


## Challenges
 Achieving the right IAM balance between security and functionality.
 Orchestrating synchronous CloudWatch‑triggered AI decisions.
 Optimizing prompt engineering for consistent reasoning from the Titan model.
 Integrating large datasets securely into the dashboard.

## Accomplishments
 Successfully built a self‑healing, autonomous AWS management agent.
 Achieved automated compliance and cost savings through Lambda + Bedrock synergy.
 Developed a real‑time, filterable dashboard integrating AI insights, PowerPipe scans, and operational logs.

## What We Learned
 Prompt engineering is key to reliable AI‑based operational decisions.
 Minimal privilege IAM design enhances both security and scalability.
 Building an event‑driven, serverless system improves responsiveness while keeping costs low.
 Combining FinOps principles with autonomous remediation yields exponential efficiency gains.​

## What’s Next
 Integrating RDS, EKS, and AWS Security Hub.
 Introducing multimodal AI reasoning (text + metrics + visuals).
 Adding smart notifications (via Slack/Email) for human‑in‑the‑loop verification.
 Expanding cross‑account support for large enterprises.

## Access the Project
### 1. Live Dashboard:

http://15.206.90.7:8501/

### 2. Source Code:
git clone https://github.com/Rajat-silvo/AI-Agent-AWS-Hackathon.git

### 3. Run Locally:

pip install -r requirements.txt

streamlit run frontend.py
