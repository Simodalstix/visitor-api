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

---

## 👨‍💻 Built By

Simon Parker  
[simostack.com](https://simostack.com)  
Passionate about backend, DevOps, and building cool, efficient tools
