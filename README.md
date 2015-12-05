### Dynamic Vagrant + Ansible provisioner ###

#### Requirements ####

* Vagrant version: 1.7.4
* Ansible version: 1.9.1
* Python: 2.7.10

#### Repository overview ####

```
#!bash
$ tree
.
├── README.md
├── Vagrantfile
├── loadtest.py
└── provisioning
    ├── common.yml
    ├── lb.yml
    ├── roles
    │   ├── common
    │   │   └── tasks
    │   │       └── main.yml
    │   ├── lb
    │   │   ├── handlers
    │   │   │   └── main.yml
    │   │   ├── tasks
    │   │   │   └── main.yml
    │   │   └── templates
    │   │       └── nginx.conf.j2
    │   └── webapp
    │       ├── handlers
    │       │   └── main.yml
    │       ├── tasks
    │       │   └── main.yml
    │       └── templates
    │           └── nginx.j2
    ├── site.yml
    └── webapp.yml

12 directories, 14 files
```

#### What will this repository install? ###

* Centos 7
* One load balancer using nginx-1.6.3 (default round-robin upstream configuration)
* Three back-end webserver nodes with nginx (Expandable to any number of webserver nodes)
* loadtest.py script (minimum Python 2.7) that runs requests against nodes to receive response back from the website 

#### What will it not do? ###

* SSL Termination
* Clean secure nginx configuration (most of the default nginx config is on the backend servers) 
* Secure vagrant keys (config.ssh.insert_key = false)

#### How do I get set up? ###

```
#!bash

git clone https://kamger@bitbucket.org/kamger/leo.git
vagrant up
```

###### Edit the Vagrantfile if you want to change:

* Domain name
* Hostnames
* Which nodes to always run provisioner on
* Memory
* Add more nodes ( Ansible will update and reload the nginx configuration for the loadbalancer)

```
# vars
domain = "example.com"
hostname_lb = "lb" # hostname for lb
hostname_backend = "webapp" # hostname for backend servers

# Nodes
# Available parameters :
# :run => "once" || "always" (blank defaults to once)
# :memory => "1024" || "512" is the default value
#
# Add new nodes here
nodes = [
  { :hostname => "#{hostname_lb}-01.#{domain}", :memory => "1024", :run => "always", :ip => "192.168.50.10"},
  { :hostname => "#{hostname_backend}-01.#{domain}", :ip => "192.168.50.21"},
  { :hostname => "#{hostname_backend}-02.#{domain}", :ip => "192.168.50.22"},
  { :hostname => "#{hostname_backend}-03.#{domain}", :ip => "192.168.50.23"},
]

groups = {
    "lb" => ["#{hostname_lb}-01.#{domain}"],
    "webapp" => [], # can't use webapp-[0:3].example.com host range pattern due to bug https://github.com/mitchellh/vagrant/issues/3539 // PR merged (Vagrant 1.8).
    "all_groups:children" => ["#{hostname_lb}", "#{hostname_backend}"],
} # we will work around this limited feature by pushing hostnames

```
#### How can I test the Load ####

* loadtest.py - Run this script with the available parameters below
* curl - Just run a plain old curl for loop

```
$ ./loadtest.py --help
usage: loadtest.py [-h] -s SERVER [-n NUMBER]

Script runs requests against given server n number of times

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Server name or Ip
  -n NUMBER, --number NUMBER
                        Number of iterations to run (default=5)
```

#####Output from running loadtest:#####

```
$ ./loadtest.py -s 192.168.50.10 -n 10

Hostname: webapp-02.example.com
Ip: 192.168.50.22
Hit counter: 3

Hostname: webapp-01.example.com
Ip: 192.168.50.21
Hit counter: 3

Hostname: webapp-03.example.com
Ip: 192.168.50.23
Hit counter: 4
```
```
$ for i in $(seq 1 20); do curl --progress -I 192.168.50.10 | awk '/X-Served-By:/ { print "Node: ", $2 }'; done

Node:  webapp-03.example.com

Node:  webapp-01.example.com

Node:  webapp-02.example.com

Node:  webapp-03.example.com

Node:  webapp-01.example.com

Node:  webapp-02.example.com
```
