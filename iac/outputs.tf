output "weaponsLeft_webhook_url" {
  value = "https://${aws_api_gateway_rest_api.weaponsLeft_api.id}.execute-api.ap-southeast-1.amazonaws.com/${aws_api_gateway_stage.prod.stage_name}"
}
