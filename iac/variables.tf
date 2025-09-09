variable "bot_token" {
  type = string
  description = "The token for the strongRight bot"
}

variable "chat_id" {
  type = string
  description = "The chat ID for the strongRight bot"
}

variable "thread_id" {
  type = string
  description = "The thread ID for the strongRight bot"
}

variable "weapons_left_bot_token" {
  description = "Telegram bot token for weaponsLeft bot"
  type        = string
  sensitive   = true
}

# pythagoras
variable "fxratesapi_key" {
  type = string
  description = "The FXRATES api key"
}

variable "telegram_token" {
  type = string
  description = "Telegram bot token for pythagoras"
}

variable "telegram_chat_id" {
  type = string
  description = "Telegram chat id"
}
