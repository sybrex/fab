# Fabric tasks

## Deployment

Settings on the remote server
-----------------------------
Account deployer with deploy key for github
https://docs.github.com/en/developers/overview/managing-deploy-keys#deploy-keys

```commandline
# /home/deployer/.ssh/config
Host fab.github.com
HostName github.com
User git
IdentityFile ~/.ssh/github_fab
```

Settings on local computer
--------------------------
SSH connection settings for deployer user
```commandline
# ~/.ssh/config
Host myserver-dep
HostName 1.1.1.1
User deployer
IdentityFile ~/.ssh/myserver_deployer_key
```