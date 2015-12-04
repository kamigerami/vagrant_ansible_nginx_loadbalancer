# by Kami Gerami 
#
#
# Domainname
domain = "example.com"

# Nodes 
# Add new nodes here
nodes = [
  { :hostname => "lb-01.#{domain}",     :memory => "512", :ip => "192.168.2.10"},
  { :hostname => "webapp-01.#{domain}", :memory => "512", :ip => "192.168.2.21"},
  { :hostname => "webapp-02.#{domain}", :memory => "512", :ip => "192.168.2.22"},
  { :hostname => "webapp-03.#{domain}", :memory => "512", :ip => "192.168.2.23"}
]

groups = {
    "lb" => ["lb-01.#{domain}"],
    "webapp" => [], # can't use webapp-[0:3].example.com host range pattern due to bug https://github.com/mitchellh/vagrant/issues/3539 // Pull Request Added.
    "all_groups:children" => ["lb", "webapp"], 
}

# generate extra_vars
hostname_ip = { }


Vagrant.configure(2) do |config|
  
  nodes.each do |node|
    # set the vars
    hostname = node[:hostname]
    memory = node[:memory]
    ip = node[:ip]
    
    # Generate the extra_vars with hostname => ip
    hostname_ip[hostname] = ip

    # Workaround for #Can't use alphanumeric patterns for box names in ansible.groups #3539 bug https://github.com/mitchellh/vagrant/issues/3539
    # Until my PR is merged : https://github.com/mitchellh/vagrant/pull/6639
    # create groups
    if hostname.include? "webapp"
      groups["webapp"].push(hostname)
    end
      
      config.vm.box = "centos/7"

      config.vm.define hostname do |config|
        config.vm.hostname = hostname
        config.vm.network :private_network, ip: ip


        config.vm.provider :virtualbox do |vb|
          vb.customize ["modifyvm", :id, "--memory", memory, "--name", hostname]
        end

        # if we want to manage hosts ip and resolver via vagrant-hostmanager plugin
        if Vagrant.has_plugin?("vagrant-hostmanager")
          config.vm.provision :hostmanager do |manager|
            manager.hostmanager.enabled = true
            manager.hostmanager.manage_host = true
            manager.hostmanager.ignore_private_ip = false
            manager.hostmanager.include_offline = true
           end
        else
          warn "vagrant-hostmanager is not installed! run vagrant plugin install vagrant-hostmanager\nif you want /etc/hosts to be managed by vagrant"
        end
 
        # ansible provisioner
        config.vm.provision :ansible do |ansible|
          ansible.playbook = "provisioning/site.yml"
          ansible.groups = groups
          ansible.sudo = true
          ansible.extra_vars = hostname_ip
        end

      end
  end    
end
