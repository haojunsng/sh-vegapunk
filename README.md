# 🤖⚙️ `data_robot`
*"SUPER!!!"*

`data_robot` is modeled after **Franky** from the Straw Hat Pirates. While Franky builds ships, this one builds bots — starting with Telegram automation.

Right now, `data_robot` is docked with two working arms (Telegram bot):

---

## 🚀 Current Abilities

### ✅ STRONG-RIGHT! (Telegram Poll Dispatcher)
`strong_right` launches a **weekly poll every Sunday night** in a Telegram group to collect running attendance availability for the upcoming week. 

### ✅ WEAPONS-LEFT! (Bill Splitter)
`weapons_left` helps groups to split bills with ease. **Simply input who paid what, and it will automatically calculate how much everyone owes - and who needs to pay whom to settle up.** Perfect for shared meals.

---
## 🛠️ Architecture & Deployment Stack

The current setup follows a **serverless-first** approach with infrastructure defined as code:

| Component          | Tech Stack           | Description                              |
|--------------------|----------------------|------------------------------------------|
| Bot logic          | Python 3.13          | Telegram API interaction and poll/bill logic  |
| Compute            | AWS Lambda           | Serverless compute (.zip archive)        |
| Scheduling         | AWS EventBridge      | Function triggered on a schedule (polls) |
| Webhook Endpoint   | HTTP API Gateway     | Receives Telegram webhook for bill split |
| Config management  | Lambda Env Vars      | Chat ID & token securely injected        |
| Deployment         | Terraform            | Infrastructure as Code (IaC)             |
| CI/CD Pipeline     | GitHub Actions       | Automated deployment via OIDC auth to S3 |

---
