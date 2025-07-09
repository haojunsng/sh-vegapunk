# Cloudflare Workers Setup Guide

Quick reference for setting up and deploying Cloudflare Workers projects.

## Initial Setup

1. **Initialize a new Worker project**
   ```bash
   npx wrangler init <project-name>
   cd <project-name>
   ```

2. **Configure environment variables**
   - Go to [Cloudflare Dashboard](https://dash.cloudflare.com) → Workers & Pages
   - Select your worker → Settings → Variables
   - Add your environment variables (secrets, API keys, etc.)

## Development Workflow

1. **Test locally during development**
   ```bash
   npx wrangler dev
   ```
   - Starts local development server
   - Hot reloads on file changes
   - Access at `http://localhost:8787`

2. **Deploy to production**
   ```bash
   npx wrangler deploy
   ```
   - Builds and deploys to Cloudflare's edge network
   - Updates your worker instantly

## Debugging & Monitoring

1. **View live logs**
   ```bash
   npx wrangler tail
   ```
   - Streams real-time logs from your deployed worker
   - Useful for debugging production issues

2. **Additional useful commands**
   ```bash
   # List all your workers
   npx wrangler whoami
   
   # View worker details
   npx wrangler whoami
   
   # Delete a worker
   npx wrangler delete <worker-name>
   ```

## Project Structure

```
<vegapunk_satellite>/
├── src/
│   └── index.js          # Main worker code
├── wrangler.jsonc        # Worker configuration
├── package.json          # Dependencies
└── README.md
```
