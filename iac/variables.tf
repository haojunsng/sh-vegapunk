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
