How to test your Ansible Deployment with Vagrant
################################################
:date: 2016-12-28 00:53
:author: Sanyam Khurana
:category: Experience
:slug: ansible-deployment-vagrant

When you start writing Ansible for automating your deployment, one common problem is about testing if it does work as you intend to do it. Some people prefer to do it directly on a server. But then it has all sorts of problems associated (for example when the no. of servers to be provisioned/deployed grows) and I clearly don't like the idea to test Ansible on servers directly. So, I chose the option to use virtual machines using Vagrant.

With Vagrant you could test complex setups like (say) having 4 machines behind a load balancer (just to start with). I've tried to both provision as well as deployment using Ansible + Vagrant. In this post, I'll be quickly covering about testing deployment using Ansible + Vagrant.

In your directory you run Vagrant init; that would provide you a Vagrantfile to start up your virtual machine. Here is a basic configuration that would enable you to boot up an ubuntu machine with a static ip which you could use later to put in your ansible host file.

.. code:: bash

    Vagrant.configure("2") do |config|
      config.vm.box = "ubuntu/trusty64"
      config.vm.network "private_network", ip: "10.0.0.10"
      config.vm.network "forwarded_port", guest: 22, host: 22
    end


Now you can boot up your virtual machine using ```vagrant up``` and try to login using ```vagrant ssh```. After ssh-ing into your virtual server; you can do `ifconfig` to verify that the IP of the server is `10.0.0.10`.

In your inventory file you can now mention the IP of the host to ```10.0.0.10```, exactly what we mentioned in the Vagrant file.

Your ansible.cfg file can be like this:

.. code:: bash

    [defaults]
    inventory = ./virtualhosts
    private_key_file = /path/to/project/deployment/.vagrant/machines/default/virtualbox/private_key
    remote_user = vagrant
    host_key_checking = False

and we'll refer the hosts as virtualhosts, so your ``virtualhosts`` inventory file would be like this:

.. code:: bash

    project_web ansible_ssh_host=10.0.0.10 ansible_ssh_port=22 ansible_ssh_user=vagrant ansible_ssh_private_key_file=/path/to/project/deployment/.vagrant/machines/default/virtualbox/private_key

    [project]
    project_web

    [project:vars]
    repo_remote=origin
    repo_branch=master
    DEPLOYMENT_TYPE=DEV


Replace the ``ansible_ssh_private_key_file`` with a valid path from your ``.vagrant`` directory.

Now try running your Ansible with 

.. code:: bash

    ansible-playbook -i virtualhosts playbook.yml


And it's done, with your ``ansible.cfg``, the private ssh key would be correctly chosen for authentication and the ``playbook`` would run by user ``vagrant``.

One can model more complex setups with lot of servers and load balancer to mimic actual deployment on servers.

