# -*- mode: ruby -*-
# vi: set ft=ruby :

# Function to dynamically get the host IP
# Used for setting the `smb_host` in config.vm.synced_folder
def get_host_ip
  # This example uses `ifconfig` and `grep` to find inet interface and host IP address
  host_ips = `ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}'`.strip.split("\n")
  host_ip = host_ips.find { |ip| ip.start_with?("192.168.") } || host_ips.first
  return host_ip
end

Vagrant.configure("2") do |config|
  
  module OS
    def OS.windows?
      (/cygwin|mswin|mingw|bccwin|wince|emx/ =~ RUBY_PLATFORM) != nil
    end
    def OS.mac?
      (/darwin/ =~ RUBY_PLATFORM) != nil
    end
    def OS.unix?
      !OS.windows?
    end
    def OS.linux?
      OS.unix? and not OS.mac?
    end
  end
  
  if OS.mac?
    
    puts "- Mac OS detected"
    puts "  -- Provider: QEMU"
    
    config.vm.box = "injae-lab/ubuntu-24.04"

    config.vm.network "forwarded_port", guest: 80, host: 8080 
    config.vm.network "forwarded_port", guest: 8000, host: 8000
    config.vm.network "forwarded_port", id: "ssh", guest: 22, host: 1243

    config.ssh.insert_key = true
    config.ssh.forward_agent = true

    # Automatically detect the SMB host IP
    smb_host_ip = get_host_ip
    
    config.vm.synced_folder "./", "/usr/local/apps/OH4S_Proteins",
    type: "smb",
    smb_host: smb_host_ip
    
    config.vm.provider "qemu" do |qe|
      qe.memory = "4096" # 4GB
    end
    
  elsif OS.linux?
    
    # Every Vagrant development environment requires a box. You can search for
    # boxes at https://vagrantcloud.com/search.
    config.vm.box = "ubuntu/focal64"
    
    # Disable automatic box update checking. If you disable this, then
    # boxes will only be checked for updates when the user runs
    # `vagrant box outdated`. This is not recommended.
    # config.vm.box_check_update = false
    
    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine. In the example below,
    # accessing "localhost:8080" will access port 80 on the guest machine.
    # NOTE: This will enable public access to the opened port
    config.vm.network "forwarded_port", guest: 80, host: 8080
    config.vm.network "forwarded_port", guest: 8000, host: 8000
    
    # Create a forwarded port mapping which allows access to a specific port
    # within the machine from a port on the host machine and only allow access
    # via 127.0.0.1 to disable public access
    # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"
    
    # Create a private network, which allows host-only access to the machine
    # using a specific IP.
    # config.vm.network "private_network", ip: "192.168.33.10"
    
    # Create a public network, which generally matched to bridged network.
    # Bridged networks make the machine appear as another physical device on
    # your network.
    # config.vm.network "public_network"
    
    # Share an additional folder to the guest VM. The first argument is
    # the path on the host to the actual folder. The second argument is
    # the path on the guest to mount the folder. And the optional third
    # argument is a set of non-required options.
    # config.vm.synced_folder "../data", "/vagrant_data"
    config.vm.synced_folder "./app", "/usr/local/apps/OH4S_Proteins/app"
    config.vm.synced_folder "./deploy", "/usr/local/apps/OH4S_Proteins/deploy"
    
    # Provider-specific configuration so you can fine-tune various
    # backing providers for Vagrant. These expose provider-specific options.
    # Example for VirtualBox:
    #
    # config.vm.provider "virtualbox" do |vb|
    #   # Display the VirtualBox GUI when booting the machine
    #   vb.gui = true
    #
    #   # Customize the amount of memory on the VM:
    #   vb.memory = "1024"
    # end
    #
    # View the documentation for the provider you are using for more
    # information on available options.
    
    # Enable provisioning with a shell script. Additional provisioners such as
    # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
    # documentation for more information about their specific syntax and use.
    # config.vm.provision "shell", inline: <<-SHELL
    #   apt-get update
    #   apt-get install -y apache2
    # SHELL
    
  elsif OS.windows?
    
    puts "Windows OS detected"
    puts "Please add configuration to VagrantFile"
    
  else
    
    puts "Unknown OS detected"
    puts "Please add configuration to VagrantFile"
    
  end
end
