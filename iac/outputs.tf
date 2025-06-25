output "weaponsLeft_webhook_url" {
  value = "${aws_api_gateway_stage.prod.invoke_url}"
}
