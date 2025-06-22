# 🤖⚙️ `data_robot`
*"SUPER!!!"*

`data_robot` is modeled after **Franky** from the Straw Hat Pirates. While Franky builds ships, this one builds bots — starting with Telegram automation.

Right now, `data_robot` is docked with only one working arm (Telegram bot).

---

## 🚀 Current Abilities

### ✅ Telegram Poll Dispatcher  
`strongRight` currently launches a **weekly poll every Sunday night** in a Telegram group to collect attendance availability for the upcoming week. 

---
## 🛠️ Architecture & Deployment Stack

The current setup follows a **serverless-first** approach with infrastructure defined as code:

| Component        | Tech Stack           | Description                              |
|------------------|----------------------|------------------------------------------|
| Bot logic        | Python 3.13          | Telegram API interaction and poll logic  |
| Serverless infra | AWS Lambda           | Function triggered on a schedule         |
| Config management| Lambda Env Vars      | Chat ID & token securely injected        |
| Deployment       | Terraform            | Infrastructure as Code (IaC)             |
| CI/CD Pipeline   | GitHub Actions       | Automated deployment via OIDC auth to S3 |

---
