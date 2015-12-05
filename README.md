# Dynamic Vagrant + Ansible provisioner #

### Requirements ###

* Vagrant version: 1.7.4
* Ansible version: 1.9.1
* Python: 2.7.10

### Repository overview ###

```
#!bash
$ tree
.
â”œâ”€â”€ Vagrantfile
â”œâ”€â”€ loadtest.py
â””â”€â”€ provisioning
    â”œâ”€â”€ common.yml
    â”œâ”€â”€ lb.yml
    â”œâ”€â”€ roles
    â”‚Â Â  â”œâ”€â”€ common
    â”‚Â Â  â”‚Â Â  â””â”€â”€ tasks
    â”‚Â Â  â”‚Â Â      â””â”€â”€ main.yml
    â”‚Â Â  â”œâ”€â”€ lb
    â”‚Â Â  â”‚Â Â  â”œâ”€â”€ handlers
    â”‚Â Â  â”‚Â Â  â”‚Â Â  â””â”€â”€ main.yml
    â”‚Â Â  â”‚Â Â  â”œâ”€â”€ tasks
    â”‚Â Â  â”‚Â Â  â”‚Â Â  â””â”€â”€ main.yml
    â”‚Â Â  â”‚Â Â  â””â”€â”€ templates
    â”‚Â Â  â”‚Â Â      â””â”€â”€ nginx.conf.j2
    â”‚Â Â  â””â”€â”€ webapp
    â”‚Â Â      â”œâ”€â”€ handlers
    â”‚Â Â      â”‚Â Â  â””â”€â”€ main.yml
    â”‚Â Â      â”œâ”€â”€ tasks
    â”‚Â Â      â”‚Â Â  â””â”€â”€ main.yml
    â”‚Â Â      â””â”€â”€ templates
    â”‚Â Â          â””â”€â”€ nginx.j2
    â”œâ”€â”€ site.yml
    â””â”€â”€ webapp.yml

12 directories, 13 files
```

### What will this repository install? ###

* Centos 7
* One load balancer using nginx-1.6.3 (default round-robin upstream configuration)
* Three back-end webserver nodes with nginx (Expandable to any number of webserver nodes)
* loadtest.py script (minimum Python 2.7) that runs threaded requests against nodes to receive response back with their -X header

### What won't it install ###

* SSL Termination

### How do I get set up? ###

```
#!bash

git clone https://kamger@bitbucket.org/kamger/leo.git
vagrant up
```

Edit the Vagrantfile if you want to change:

* Domain
* Which nodes to always run provisioner on
* Memory
* Add more nodes ( Ansible will update and reload the nginx configuration for the loadbalancer)

```
#!ruby


domain = "example.com"

# Nodes
# Available parameters :
# :run => "once" || "always" (blank defaults to once)
# :memory => "1024" || "512" is the default value
#
# Add new nodes here
nodes = [
  { :hostname => "lb-01.#{domain}", :memory => "1024", :run => "always", :ip => "192.168.2.10"},
  { :hostname => "webapp-01.#{domain}", :ip => "192.168.2.21"},
  { :hostname => "webapp-02.#{domain}", :ip => "192.168.2.22"},
  { :hostname => "webapp-03.#{domain}", :ip => "192.168.2.23"},
  { :hostname => "webapp-04.#{domain}", :ip => "192.168.2.24"},
  { :hostname => "webapp-05.#{domain}", :ip => "192.168.2.25"},
]

groups = {
    "lb" => ["lb-01.#{domain}"],
    "webapp" => [], # can't use webapp-[0:3].example.com host range pattern due to bug https://github.com/mitchellh/vagrant/issues/3539 // Pull Request Added.
    "all_groups:children" => ["lb", "webapp"],
}

```
### Testing Load ###

* loadtest.py - Run this script with the available parameters below

```
#!python
$ ./loadtest.py --help
usage: loadtest.py [-h] -s SERVER [-n NUMBER] [-t THREAD]

Script runs threaded requests against given server n number of times

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Server name or Ip
  -n NUMBER, --number NUMBER
                        Number of iterations to run (default=5)
  -t THREAD, --thread THREAD
                        Thread count (default=2)
```

Output from running loadtest:

```
#!python

$ ./loadtest.py -s 192.168.2.10 -n 5 -t 2

$ ./loadtest.py -s 192.168.2.10
Thread nr: 1
Host: webapp-05.example.com
Hit counter: 1

Thread nr: 1
Host: webapp-02.example.com
Hit counter: 1

Thread nr: 1
Host: webapp-04.example.com
Hit counter: 1

Thread nr: 1
Host: webapp-01.example.com
Hit counter: 1

Thread nr: 1
Host: webapp-03.example.com
Hit counter: 1
```
