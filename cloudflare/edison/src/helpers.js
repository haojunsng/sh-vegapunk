const weatherCodeMap = {
	0: "Clear sky",
	1: "Mainly clear",
	2: "Partly cloudy",
	3: "Overcast",
	45: "Fog",
	51: "Light drizzle",
	53: "Moderate drizzle",
	55: "Dense drizzle",
	61: "Slight rain",
	63: "Moderate rain",
	65: "Heavy rain",
	80: "Slight rain showers",
	81: "Moderate rain showers",
	82: "Violent rain showers",
	95: "Thunderstorm"
}

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
	const openmeteo = data.openmeteo
	const town = data.town

	const capitalised_town = town.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
	const current_datetime = new Date().toLocaleString("en-SG", { timeZone: "Asia/Singapore" })

	return `📍 Weather for ${capitalised_town}:

${current_datetime}

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

🌦 OpenMeteo Weather:
• ${weatherCodeMap[openmeteo.weathercode]}
• Wind Speed: ${openmeteo.windspeed}km/h
• Temperature: ${openmeteo.temperature}°C

🤖 Powered by Edison 🤖
`
}
