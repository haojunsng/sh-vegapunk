import { Hono } from 'hono'

const app = new Hono()

// Telegram webhook route
app.post('/webhook', async (c) => {
	// 1. Verify Telegram secret token
	const sentToken = c.req.header('x-telegram-bot-api-secret-token')
	if (sentToken !== c.env.TELEGRAM_SECRET_TOKEN) {
		return c.text('Unauthorized', 401)
	}

	// 2. Forward the request to AWS API Gateway
	const body = await c.req.text()
	const resp = await fetch(c.env.API_GATEWAY_URL, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body
	})
	return new Response(await resp.text(), { status: resp.status })
})

export default app
