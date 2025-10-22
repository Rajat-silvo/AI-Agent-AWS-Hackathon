# CloudWise: AI Agents for AWS Cost & Compliance Optimization
## Your intelligent AWS co‑pilot for cost and security optimization.

## Inspiration
Up to 40% of a DevOps engineer’s time is spent silencing or triaging false CloudWatch alarms, often leading to wasted effort, increased costs, and reduced focus on high-value tasks. CloudWise emerged to solve this recurring inefficiency through AI‑driven intelligence that automates monitoring, remediation, and compliance management in AWS environments.

## What It Does
CloudWise continuously monitors your AWS environment for:
Cost inefficiencies: Detects idle EC2 instances and shuts them down.
Compliance risks: Scans S3 buckets for public exposure.
Automation: Executes remediation actions via Lambda functions.
Visualization: Displays savings, compliance status, and AI reasoning through a Streamlit dashboard in real time.
At its core lies Amazon Bedrock’s Titan Model, which reasons about system events, ranks alerts, and recommends or executes actions — transforming reactive tasks into proactive optimization.

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


Challenges
Achieving the right IAM balance between security and functionality.
Orchestrating synchronous CloudWatch‑triggered AI decisions.
Optimizing prompt engineering for consistent reasoning from the Titan model.
Integrating large datasets securely into the dashboard.

Accomplishments
Successfully built a self‑healing, autonomous AWS management agent.
Achieved automated compliance and cost savings through Lambda + Bedrock synergy.
Developed a real‑time, filterable dashboard integrating AI insights, PowerPipe scans, and operational logs.

What We Learned
Prompt engineering is key to reliable AI‑based operational decisions.
Minimal privilege IAM design enhances both security and scalability.
Building an event‑driven, serverless system improves responsiveness while keeping costs low.
Combining FinOps principles with autonomous remediation yields exponential efficiency gains.​

What’s Next
Integrating RDS, EKS, and AWS Security Hub.
Introducing multimodal AI reasoning (text + metrics + visuals).
Adding smart notifications (via Slack/Email) for human‑in‑the‑loop verification.
Expanding cross‑account support for large enterprises.

Access the Project
1. Live Dashboard:


http://15.206.90.7:8501/
2. Source Code:
git clone https://github.com/<your-username>/<your-repo-name>.git
3. Run Locally:
bash
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
