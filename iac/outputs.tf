output "weaponsLeft_webhook_url" {
  value = "${aws_apigatewayv2_stage.prod.invoke_url}"
}
