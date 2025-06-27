# 🤖⚙️ `sh-vegapunk`

<div align="center">
  <img width="370" alt="image" src="https://github.com/user-attachments/assets/3c547c52-70fa-4a8f-81b6-fcf703c7ce93" />
</div>

<p align="center">
  <code>sh-vegapunk</code> is modeled after <strong>Vegapunk</strong> from the One Piece.
</p>


## 🚀 Satellites Available

### ✅ SHAKA! (Telegram Poll Dispatcher)
<div align="center">
  <img width="50%" src="https://github.com/user-attachments/assets/8dfe8b73-f0f9-4d2b-be9c-be3cf48798fe" />
</div>

`SHAKA` launches a **weekly poll every Sunday night** in a Telegram group to collect running attendance availability for the upcoming week. 

#### Architecture
<div align="center">
  <img height="400" width="200" alt="image" src="https://github.com/user-attachments/assets/32d578f2-fa83-4fe0-85d6-f72f6f1014f1" />
</div>

**Tech Stack:**
- **Compute:** AWS Lambda (Python 3.13)
- **Scheduling:** AWS EventBridge (weekly trigger)
- **Deployment:** Terraform + GitHub Actions

---

### ✅ LILITH! (Bill Splitter)

<div align="center">
  <img width="30%" alt="Telegram Bot Demo" src="media/demo-lilith.gif" />
</div>

`LILITH` helps groups to split bills with ease. **Simply input who paid what, and it will automatically calculate how much everyone owes - and who needs to pay whom to settle up.** Perfect for shared meals.

#### Architecture
<div align="center">
  <img height="400" width="450" alt="image" src="https://github.com/user-attachments/assets/eceb87af-40ab-43a9-9be5-c98521894f9c" />
</div>

**Tech Stack:**
- **Compute:** AWS Lambda (Python 3.13)
- **Webhook Endpoint:** AWS API Gateway (REST API)
- **Reverse Proxy:** Cloudflare Worker
  - **Runtime:** JavaScript
  - **CLI Tool:** Wrangler (Cloudflare's deployment tool)
  - **Package Manager:** npm/Node.js
- **Deployment:** Terraform + GitHub Actions

#### Security Features
- **IP Whitelisting:** API Gateway protected by resource policy allowing only [Cloudflare IP ranges](https://www.cloudflare.com/ips/)
- **Secret Verification:** Worker validates `X-Telegram-Bot-Api-Secret-Token` header
- **Hidden Endpoint:** AWS API endpoint never exposed directly to Telegram

---

## 🛠️ Infrastructure & Deployment

The current setup follows a **serverless-first** approach with infrastructure defined as code:

| Component          | Technology           | Purpose                                |
|--------------------|----------------------|----------------------------------------|
| Application Logic  | Python 3.13          | Bot business logic and Telegram API    |
| Compute Runtime    | AWS Lambda           | Serverless function execution          |
| Event Scheduling   | AWS EventBridge      | Cron-based trigger for polls           |
| API Gateway        | AWS API Gateway      | REST API endpoint for webhooks         |
| Security Layer     | Cloudflare Workers   | Reverse proxy with IP whitelisting     |
| Configuration      | Environment Variables| Secure token and chat ID management    |
| Infrastructure     | Terraform            | Infrastructure as Code (IaC)           |
| CI/CD              | GitHub Actions       | Automated deployment pipeline          |

---
