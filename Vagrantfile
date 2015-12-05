# by Kami Gerami 
#
#
Vagrant.require_version ">= 1.7.2"

# Domainname
domain = "example.com"

# Nodes 
# Available parameters : 
# :run => "once" || "always" (blank defaults to once)
# :memory => "1024" || "512" is the default value
#
# Add new nodes here
nodes = [
  { :hostname => "lb-01.#{domain}", :memory => "1024", :run => "always", :ip => "192.168.50.10"},
  { :hostname => "webapp-01.#{domain}", :ip => "192.168.50.21"},
  { :hostname => "webapp-02.#{domain}", :ip => "192.168.50.22"},
  { :hostname => "webapp-03.#{domain}", :ip => "192.168.50.23"},
]

groups = {
    "lb" => ["lb-01.#{domain}"],
    "webapp" => [], # can't use webapp-[0:3].example.com host range pattern due to bug https://github.com/mitchellh/vagrant/issues/3539 // PR merged (Vagrant 1.8).
    "all_groups:children" => ["lb", "webapp"], 
}

# Empty hash to generate extra_vars dynamically
hostname_ip = Hash.new { |hash, key| hash[key] = [] }


Vagrant.configure(2) do |config|
  
  nodes.each do |node|
    # Set the vars
    hostname = node[:hostname]
    ip = node[:ip]
    memory = node[:memory] || "512" # set 512 as default if nothing else is set
    run = node[:run] || "always" # set to provision always if nothing else is set

    # Add the extra_vars with hostname => ip
    hostname_ip[:ip] << node
    #
    # Workaround for #Can't use alphanumeric patterns for box names in ansible.groups #3539 bug https://github.com/mitchellh/vagrant/issues/3539
    # PR is merged ( vagrant 1.8) : https://github.com/mitchellh/vagrant/pull/6639

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

        # ansible provisioner
        config.vm.provision :ansible, run: run do |ansible|
          ansible.playbook = "provisioning/site.yml"
          ansible.groups = groups
          ansible.sudo = true
          ansible.extra_vars = hostname_ip
        end

      end
  end    
end
