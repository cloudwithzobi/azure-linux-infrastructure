output "public_ip_address" {
  description = "Public IP of the VM"
  value       = azurerm_public_ip.main.ip_address
}

output "ssh_command" {
  description = "Command to SSH into the VM"
  value       = "ssh -i ~/.ssh/azure_phase1 azureuser@${azurerm_public_ip.main.ip_address}"
}

output "resource_group_name" {
  description = "Resource group name"
  value       = azurerm_resource_group.main.name
}
