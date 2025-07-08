export async function sendTelegramMessage(c, chatId, text) {
	const telegramUrl = `https://api.telegram.org/bot${c.env.BOT_TOKEN}/sendMessage`
	try {
	  const resp = await fetch(telegramUrl, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({
		  chat_id: chatId,
		  text,
		}),
	  })
  
	  if (!resp.ok) {
		const errorBody = await resp.text()
		console.error(`Telegram API error: ${resp.status} - ${errorBody}`)
		throw new Error(`Telegram API responded with status ${resp.status}`)
	  }
	} catch (error) {
	  console.error('Failed to send Telegram message:', error)
	  throw error
	}
  }

export function formatWeatherMessage(data) {
	const tomorrow = data.tomorrow_io
	const google = data.google

	return `📍 Weather for ${data.town}:

🌦 Tomorrow.io:
• Rain Intensity: ${tomorrow.rainIntensity}
• Humidity: ${tomorrow.humidity}%
• Precipitation: ${tomorrow.precipitationProbability}%
• Temperature: ${tomorrow.temperature}°C

🌦 Google Weather:
• ${google.description}
• Humidity: ${google.humidity}%
• Precipitation: ${google.precipitationProbability}%
• Temperature: ${google.temperature}°C
`
}
