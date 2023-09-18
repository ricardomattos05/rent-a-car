resource "azurerm_virtual_machine" "vm" {
  name                  = "DashVM"
  location              = var.location
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.nic.id]
  vm_size               = "Standard_B1s"

  storage_os_disk {
    name              = "DashOSDisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Premium_LRS"
  }

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  os_profile {
    computer_name  = "DashHostName"
    admin_username = var.admin_username
    admin_password = var.admin_password
  }

  os_profile_linux_config {
    disable_password_authentication = true
    ssh_keys {
      path     = "/home/${var.admin_username}/.ssh/authorized_keys"
      key_data = file("~/.ssh/id_rsa.pub")
    }
  }

  provisioner "local-exec" {
    command = "sleep 30"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y docker.io",
      "sudo systemctl start docker",
      "sudo systemctl enable docker",
      "sudo apt-get install -y docker-compose",
      "sudo docker login RentcarDash.azurecr.io -u ${azurerm_container_registry.acr.admin_username} -p ${azurerm_container_registry.acr.admin_password}",
      "sudo docker pull RentcarDash.azurecr.io/sua-imagem:versao"
    ]

    connection {
      type        = "ssh"
      user        = var.admin_username
      password    = var.admin_password
      host        = azurerm_public_ip.pip.ip_address
      agent       = false
      private_key = file("~/.ssh/id_rsa")
    }
  }

  provisioner "file" {
    source      = "../docker-compose.yml"
    destination = "/home/${var.admin_username}/docker-compose.yml"
    connection {
      type        = "ssh"
      user        = var.admin_username
      password    = var.admin_password
      host        = azurerm_public_ip.pip.ip_address
      agent       = false
      private_key = file("~/.ssh/id_rsa")
    }
  }

  provisioner "remote-exec" {
    inline = [
      "cd /home/${var.admin_username}",
      "docker-compose up -d"
    ]

    connection {
      type        = "ssh"
      user        = var.admin_username
      password    = var.admin_password
      host        = azurerm_public_ip.pip.ip_address
      agent       = false
      private_key = file("~/.ssh/id_rsa")
    }
  }
  depends_on = [azurerm_public_ip.pip]
}
