### /srv/salt/base/robomussels.sls ###
#####################################

install-repos:
  file:
    - managed
    - source: salt://base/files/repos/mongodb.jin
    - name: /etc/yum.repos.d/mongodb.repo
    - template: jinja

# add files for security
set_sshd:
  file:
    - managed
    - source: salt://base/files/security/sshd_config.jin
    - name: /etc/ssh/sshd_config
    - template: jinja
set_sudoers:
  file:
    - managed
    - source: salt://base/files/security/sudoers.jin
    - name: /etc/sudoers
    - template: jinja
base-iptables:
  pkg:
    - installed
    - name: iptables
  file:
    - managed
    - source: salt://base/files/security/iptables.jin
    - name: /etc/sysconfig/iptables
    - template: jinja
    - require:
      - pkg: base-iptables
  service:
    - running
    - enable: True
    - name: iptables
    - require:
      - pkg: base-iptables
    - watch:
      - file: base-iptables
  cmd:
    - run
    - name: service iptables restart
    - require:
      - file: base-iptables

salt-minion:
  pkg:
    - installed
    - name: salt-minion
  service:
    - running
    - enable: Trueserv
    - name: salt-minion
    - require:
      - pkg: salt-minion

#######################################
#######################################

install-basic:
  # Install prerequisites
  pkg:
    - installed
    - names:
      - git
      - nano
      - man
      - htop
      - iftop
      - tcpdump
      - python
      - nmap
      - fail2ban
      - wget
      - nc
      - telnet
      - mongodb-org
      - nginx
      - vsftpd

#######################################
#######################################

blieberman:
  user.present:
    - fullname: Ben Lieberman
    - shell: /bin/bash
    - home: /home/blieberman
    - uid: 300
    - groups:
      - wheel

AAAAB3NzaC1yc2EAAAADAQABAAABAQDM8+62VdEnGDkQIZsKfEDvmXjXdv0q1Ulpk5o0deI2Jkz/bD2D20wjSBXr6e8tign1ssB2r3UifkiY81/vNdJ95rFeA23M6QJwKFrB5nx7T8xvAfXbx4hWQNr+A3cvo4o+UIRX2k8WDzuhoFj3HozC+g+/0LlYn6ROkzPrOMVFpJJJVS739/JoGbE8jQT0ocyXx8XA6MlTcp0essN+UZ4mXSNwMXKwKmlCPFSNzpKIRDVZIK8DXV20foL3VwSnOlsbSfhtH2g3ZwAdty1dnSqNkbxc9U5kc4SrCOPB4bEZ1r3cSsY+68sU2Y3YjZwI8NxSuYG+4m6y9LrPILnKCU8t blieberman@brandywine.net:
  ssh_auth:
    - present
    - user: blieberman
    - enc: ssh-rsa

tseeber:
  user.present:
    - fullname: Tiffany Seeber
    - shell: /bin/bash
    - home: /home/tseeber
    - uid: 301
    - groups:
      - wheel

AAAAB3NzaC1yc2EAAAADAQABAAACAQDJ8R6Rqzzj0df7OwngKDne6WvH22wltkv9bATQCdSQYeDOpGOtJmH1fcyBf9IVAoQY51omKhii0oj/ZtMAvf67T5Odx7oehWlgXrIU71nOXG6QZZgp4J2NVCQAHlNcszj3jP/zOJWHUgAGzBfyt4H1rqBUcc5zXfefu3ttgb1sWp4KoIOe9CWgzoh8JoHycETT8ej9sIJZxmxqr9p2fBv82qYnlDK89GmE9Qk8OQHpe4MmIZS+tfWaQfy0YNIhjGvW95tvUH6oudKk483LjSvHb0/YWNWN5S/9kiM1jF2hU7NDdaTaPD4qQ8o9FE2JggcDWTotQToKPCIGgcYtkjvSiypUM1yDGJqGRAGnEgb6p59x9CD6GhBduCjhGItTqyvsbwfeg1/mm9myRkkWiJdt3b/K1c2gjyRBPeXh0O6L8a0lmbxbhnwWnHbGCdYP2gX6PunuuUn8RutJLQNFGbdqVjUm0pCGcy60p/XK0k5QENJSYCIDGqzQJKF2l1nRKJdQa7UQ9L/X6DAB2Pl0xOAT3NFhjQjefPgiUa6uOKOMXzktz7SMbHvrhQCn1QJTOy2A8iH48JCzMTecwkVyVwRHBcGhY5FPuswKCfd9BGgbjXBgiRyoah05EbqCGZdeQH25v3RBaqjhPBldg5nuql+B6/NFA03Mtt0LQ1a1wepq2w== seeber.t@husky.neu.edu:
  ssh_auth:
    - present
    - user: tseeber
    - enc: ssh-rsa

group6:
  user.present:
    - fullname: Group 6 FTP Service Account
    - shell: /sbin/nologin
    - home: /var/www/robo
    - uid: 500
    - password: $6$BXhsWIBe$DEE2o6VefTsMGYwtnkgNjA1RX4Vr3LgvjRAqg2/t4M2W0Ne7Agvcu0bpnsrLwwruzAlwaRfSWHBqEVihQHN1F.

#######################################
#######################################

mongo-customizations:
  # place a custom mongodb config
  file:
    - managed
    - source: salt://base/files/mongodb/mongod.conf.jin
    - name: /etc/mongod.conf
    - template: jinja
  service:
    - running
    - enable: Trueserv
    - name: mongod
    - require:
      - pkg: mongodb-org

nginx-core-customizations:
  # place a customized nginx config
  file:
    - managed
    - source: salt://base/files/nginx/nginx.conf.jin
    - name: /etc/nginx/nginx.conf
    - template: jinja
    - require:
      - pkg: nginx
  service:
    - running
    - enable: Trueserv
    - name: nginx
    - require:
      - pkg: nginx

nginx-robo-www-customizations:
  # place customized nginx htaccess credentials
  file:
    - managed
    - source: salt://base/files/nginx/robo_htpasswd.jin
    - name: /etc/nginx/.robo_htpasswd
    - template: jinja
    - require:
      - pkg: nginx
  service:
    - running
    - enable: Trueserv
    - name: nginx
    - require:
      - pkg: nginx

nginx-www-customizations:
  # place a customized nginx config
  file:
    - managed
    - source: salt://base/files/nginx/robo-www.conf.jin
    - name: /etc/nginx/conf.d/robo-www.conf
    - template: jinja
    - require:
      - pkg: nginx
  service:
    - running
    - enable: Trueserv
    - name: nginx
    - require:
      - pkg: nginx

nginx-api-customizations:
  # place a customized nginx config
  file:
    - managed
    - source: salt://base/files/nginx/robo-api.conf.jin
    - name: /etc/nginx/conf.d/robo-api.conf
    - template: jinja
    - require:
      - pkg: nginx
  service:
    - running
    - enable: Trueserv
    - name: nginx
    - require:
      - pkg: nginx

vsftpd:
  service:
    - running
    - enable: Trueserv
    - name: vsftpd
    - require:
      - pkg: vsftpd

#######################################
#######################################

/var/www/robo:
  file.directory:
    - user: group6
    - group: nginx
    - mode: 755
    - makedirs: True
    - recurse:
      - user
      - group

#######################################
#######################################

run-app:
  # Use 'forever' to start the server
  cmd:
    - run
    - name: forever start --watch ./bin/www
    - cwd: /root/robomussels/node_files/robomussels
