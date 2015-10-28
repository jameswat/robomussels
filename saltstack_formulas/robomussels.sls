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
      - httpd
      - vsftpd

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

set_mongo:
# mongod customizations
  file:
    - managed
    - source: salt://base/files/mongodb/mongod.conf.jin
    - name: /etc/mongod.conf
    - template: jinja

mongodb:
  service:
    - running
    - enable: Trueserv
    - name: mongod
    - require:
      - pkg: mongodb-org

httpd:
  service:
    - running
    - enable: Trueserv
    - name: httpd
    - require:
      - pkg: httpd

vsftpd:
  service:
    - running
    - enable: Trueserv
    - name: vsftpd
    - require:
      - pkg: vsftpd
