# Simple Ansible dynamic inventory file for lightsail

EC2 plugin is awesome, but sometimes you need to use [Lightsail](https://aws.amazon.com/lightsail/).
Sometimes in need to be run from Gitlab CI.

## Example equecution

``` bash
export AWS_KEY_ID=xxxx
export AWS_ACCESS_KEY=xxx
export ENV_TAG=xxx
ansible-playbook -i lightsail.py playbook.yaml
```

## Gitlab CI example

```yaml 
image: ubuntu:latest

stages:
  - deploy
  
stage_numer_1:
  variables:
    AWS_KEY_ID: $AWS_ID
    AWS_ACCESS_KEY: $AWS_KEY
    ENV_TAG: php-prod-group
  stage: deploy
  before_script:
    - apt update
    - apt install openssh-client -y
    - eval $(ssh-agent -s)
    - ssh-add <(echo "$SSH_PRIVATE_KEY" | base64 -d)
    - apt-get update && apt-get install -y ssh python3 python3-pip
    - pip3 install boto3 ansible
  script:
    - echo "Deploying to environment"
    - ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i lightsail.py playbook.yaml
    - echo "Deploy to test was successful"
```
