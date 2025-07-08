import { Hono } from 'hono'
import { sendTelegramMessage, formatWeatherMessage } from './helpers.js'

const app = new Hono()

// Telegram webhook route
app.post('/webhook', async (c) => {
	const sentToken = c.req.header('x-telegram-bot-api-secret-token')
	if (sentToken !== c.env.TELEGRAM_SECRET_TOKEN) {
		return c.text('Unauthorized', 401)
	}

	const body = await c.req.json()
	const text = body?.message?.text?.trim().toLowerCase();
	const chatId = body?.message?.chat?.id;

	if (text === '/start' || text === '/help') {
		const welcomeMessage = `Hello! I'm Edison! Send me the name of any Singapore town and I'll tell you the latest weather.`;
		await sendTelegramMessage(c, chatId, welcomeMessage)

		return c.text('Welcome message sent', 200);
	}

	if (!text) {
		await sendTelegramMessage(c, chatId, "Please send a Singapore town name or use /help.")
		return c.text("Invalid input", 400);
	}

	const town = body?.message?.text?.trim()
	if (!town) {
		return c.text('Invalid request: Please send a town!', 400);
	}

	// Forward the request to sh-nami API
	const apiKey = c.env.API_KEY
	const encodedTown = encodeURIComponent(town)
	const completeApiUrl = `${c.env.API_URL}?town=${encodedTown}`
	
	let weatherData
	try {
		const resp = await fetch(completeApiUrl, {
			method: 'GET',
			headers: {
				'X-API-KEY': apiKey,
				'Content-Type': 'application/json'
			}
		})

		if (!resp.ok) {
			throw new Error(`Weather API returned ${resp.status}`)
		}

		weatherData = await resp.json()
	} catch (err) {
		await sendTelegramMessage(c, chatId, `Apologies. I could not fetch the weather for "${text}".`)
		return c.text('Weather fetch failed', 500)
	}

	const message = formatWeatherMessage(weatherData)
	await sendTelegramMessage(c, chatId, message)

	return c.text("Weather sent", 200)

})

export default app
