# 🛰️ Visitor Counter API

This is a lightweight, serverless visitor counter backend that powers the live traffic stats on [simostack.com](https://simostack.com) — my personal portfolio site.

Built with:

- 🐍 **Python 3.11**
- 🔗 **AWS Lambda** (via AWS SAM)
- 🧠 **DynamoDB** for fast, low-cost storage
- 🛡️ **API Gateway** with key-based protection
- 🌐 **CORS-enabled** for browser-side fetches
- 📓 **Visitor logs** include IP address, timestamp, and user-agent

---

## 🔍 How It Works

When a user visits my site:

1. My frontend JavaScript sends a `GET` request to this API's `/count` endpoint.
2. The Lambda function:
   - Increments a counter in DynamoDB
   - Logs the visitor's IP, timestamp, and user-agent
3. The updated visitor count is displayed in real time.

---

## 💡 Features

- ✅ Real-time visitor tracking
- ✅ Serverless and scalable (on-demand Lambda execution)
- ✅ Single-table DynamoDB design (counter + logs in one table)
- ✅ Logging script to view recent visits
- ✅ Optional API Key protection with referrer validation (coming soon)
- ✅ Easily extendable for geolocation, charting, or TTL cleanup

---

## 📁 Project Structure

```
.
├── app.py            # Lambda function code
├── template.yaml     # SAM template to deploy everything
├── read_logs.py      # CLI script to view logged visits
└── .env              # API key & URL (not committed)
```

---

## 🚀 Live Deployment

The API is deployed via [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/) using:

```bash
sam build && sam deploy
```

> Visit my portfolio: [simostack.com](https://simostack.com)

# 🛠️ SAM Deployment Retrospective: Issues Faced & How to Avoid Them

This doc captures all the bumps we hit deploying a simple Flask-to-Lambda visitor counter using AWS SAM, and how to avoid them next time.

---

## ✅ Final Setup Overview

- **Frontend**: simostack.com (static HTML)
- **Backend**: Python 3.11 Lambda + API Gateway + DynamoDB
- **Infra as Code**: AWS SAM (template.yaml)
- **Security**: API Key via Usage Plan
- **Extras**: CORS headers, IP logging, GitHub Actions for frontend deploy

---

## ❗ Full Troubleshooting Summary

### 1. **Missing `VisitorTable` from template.yaml**

**Symptom:** SAM deploy deleted the DynamoDB table.

- **Root Cause:** A version of `template.yaml` omitted the `VisitorTable` resource, so SAM deleted it during deploy.
- **Avoid:** Never remove critical resources unless you intend to delete them. Version control your `template.yaml` carefully.

---

### 2. **SAM deploy didn't recreate table item (`visitor_count`)**

**Symptom:** Internal Server Error until we manually added the item.

- **Avoid:** Add a `put_item()` safeguard or create it manually in DynamoDB Console after first deploy.

---

### 3. **Unclear resource-to-auth hierarchy in API Gateway**

**Symptom:** Multiple issues with API Key and Usage Plan not linking properly.

- **Root Cause:** Usage Plan must explicitly link:
  - ✅ An API Key
  - ✅ A REST API + Stage
- **Avoid:** Always check:

```bash
aws apigateway get-usage-plan --usage-plan-id <id>
```

And validate `apiStages` + API Key association.

---

### 4. **Missing Usage Plan attachment for API Key**

**Symptom:** API Key exists, but requests still return 403/Forbidden.

- **Fix:**

```bash
aws apigateway create-usage-plan-key \
  --usage-plan-id <plan-id> \
  --key-id <api-key-id> \
  --key-type API_KEY
```

- **Avoid:** Double-check if the keyType is actually `API_KEY` and not `None`:

```bash
aws apigateway get-usage-plan-keys --usage-plan-id <id>
```

---

### 5. **`NameError: event not defined` crash**

**Symptom:** Internal Server Error, but no logs until deep log inspection.

- **Root Cause:** Accessing `event['headers']` **outside** of the `lambda_handler()` function.
- **Avoid:** Never use event/context outside the handler. SAM deploy will not catch this — it crashes at init phase.

---

### 6. **API Gateway endpoint changed unexpectedly**

**Symptom:** JS fetch and curl commands failed after a redeploy.

- **Root Cause:** Changing the logical ID of the `AWS::Serverless::Api` or deleting the stack.
- **Avoid:** Keep your logical ID consistent (e.g., `VisitorApi`) so the API Gateway stays stable across deployments.

---

### 7. **API Key still gave Forbidden (missing Usage Plan)**

**Symptom:** Despite having the key in .env, requests returned 403.

- **Root Cause:** You created the API Key but forgot to attach it to a usage plan.
- **Avoid:** Always create:
  - Usage Plan → attach API Key
  - Usage Plan → attach API + Stage

---

### 8. **VS Code or WSL not detecting Python 3.11**

**Symptom:** `sam build` failed with `PythonPipBuilder` error.

- **Fix:** Ensure Python 3.11 and pip are installed and available on PATH:

```bash
sudo apt install python3.11 python3.11-venv
```

- **Avoid:** Always activate your venv:

```bash
source .venv/bin/activate
```

---

### 9. **Trying to read logs before Lambda actually invoked**

**Symptom:** Log stream existed but was stale — made debugging confusing.

- **Avoid:** Only check logs **after** a fresh `curl` call with an API key. Check timestamp vs your local clock.

---

## 😬 SAM vs Manual Deploy: Is It Worth It?

**SAM Pros:**

- Clean reproducibility
- Handles IAM, permissions, linking
- Perfect for version-controlled infra

**SAM Cons (when learning):**

- Hard to debug if you don’t know the CloudFormation lifecycle
- Unintuitive connection between API Gateway parts (API, stage, usage plan)
- Errors feel more opaque than doing it manually

**Verdict:** Now that you’ve ironed out the issues, it’ll be smoother from here on. Consider saving this `template.yaml` as your own boilerplate.

Let me know if you want a printable PDF of this or to turn it into a GitHub wiki! ✅

---

## 👨‍💻 Built By

Simon Parker  
[simostack.com](https://simostack.com)  
Passionate about backend, DevOps, and building cool, efficient tools
