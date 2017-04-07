Vagrant.configure(2) do |config|
  config.vm.box = "uhashicorp/precise64"

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provider "virtualbox" do |vb|
vb.memory = "1024"
  end

  config.vm.provision "shell", inline: <<-SHELL
sudo apt-get update
sudo apt-get install -y python3-pip
sudo pip3 install honcho
sudo pip3 install flask
  SHELL
end
