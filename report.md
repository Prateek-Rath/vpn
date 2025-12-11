# VPN Implementation with Virtual Network Functions

## Index

1) [Introduction](#introduction)
2) [Application](#application)
3) [Devops Components](#devops-components)
4) [Steps to Run](#steps-to-run)
5) [Authors](#authors)

## Introduction

A Virtual Network Function (VNF) is essentially a software implementation of a network function like a firewall, router, load balancer, VPN, etc. that runs on virtualized hardware instead of dedicated appliances,
and can be scaled, orchestrated, and deployed using various DevOps tools and techniques. In this project we have tried to implement a simple VPN along with a reverse proxy as virtual network functions, which we 
then deploy and monitor using various software tools.

## Application

The basic idea is to have an application which runs on a protected network i.e. is not visible/accessible externally. Users who wish to access the application need to connect to the VPN first which is on
the same network as the application, after which all requests to the application are forwarded through the VPN. We also add an Nginx reverse proxy at the front which takes all requests, filters out unwanted ones,
and performs basic rate limiting.

### Target App

This is a simple FastAPI application which is not externally exposed. It has just one functional endpoint `/status`, which returns an `OK` when requested.

### VPN

The core VPN implementation. Users can connect to the VPN via providing their credentials, after which they are able to access the above application. When they disconnect, they are unable to access it again.

### Nginx

We add a reverse proxy in front of the VPN for protection. It filters out any unwanted requests, and prevents the VPN from being bombarded via some rate limiting. It also becomes a central point for all requests
so that the the VPN and the target application can remain unexposed externally.

## Devops Components

We've used a modular architecture, with each of the above components as a separate service with it's own Docker containers, with Kubernetes as the orchestration mechanism and Dockerhub as the container registry.
We've also added tools like Prometheus and Grafana for monitoring metrics, and the ELK stack (Elasticsearch, Logstash, Kibana) with Filebeat, for logging. Furthermore, we've used Jenkins for continuous integration and deployment (CI/CD), and Ansible for
infrastructure automation.

![Architecture](assets/arch.png)

### Containerization and Orchestration

### Monitoring

### Logging

### CI/CD

We've used Jenkins for continuous integration and continuous deployment. On each push to any of the github branches, a webhook triggers the pipeline, which checks out the recent commits, builds the updated images for the app and vpn, and pushes them to a Docker Hub registry. It then runs the ansible playbook locally.

### Infrastructure

We've used Ansible for configuration management and infrastructure automation. When triggered via the Jenkins pipeline, ansible first stops the existing minikube cluster and starts a fresh one with specified memory and CPU requirements. It then pulls the required images from Docker Hub, and applies all k8s manifests following which the application is deployed. Since minikube with the docker driver does not expose ports externally, we need to do port forwarding, which is also done via the playbook. Finally, the application entrypoint (Nginx->VPN), Grafana for checking metrics, and Kibana for checking logs, are available on separate ports

#### Roles in Ansible

Ansible roles are useful to make the playbook smaller and easier to read. They split tasks into independent logical units which improves modularity, reusability and scalability. Since we had 3 namespaces `app`, `monitoring` and `logging`, we decided to have 4 roles, one for each plus one extra which creates these namespaces. This helped us to group deployments by their purpose, simplified the playbook, and will be easier to maintain in future when more functionalities might get added.

#### Ansible Vault

Ansible vault allows us to encrypt sensitive data such as passwords, API keys or other credentials within the project. We had a list of username-password pairs which were used to connect to the VPN. These were originally stored in a plain JSON file withing the project, which is highly insecure. We then moved it to secrets.yaml in k8s which injected them at runtime, however they were still stored in plaintext. Ansible vault allows us to encrypt these secrets securely, and while running the playbook, a password or a password file can be provided to decrypt these secrets back. This is done using a Jinja2 template which renders the k8s secret from the vault file, and during playbook execution, ansible injects decrypted credentials from the vault file into the template which is then applied to k8s.

We can encrypt the secrets as

```
ansible-vault encrypt ansible/group_vars/all/vpn_creds.yml --vault-password-file password.txt
```

and then we can put

```
ansible-playbook -i inventory.ini playbook.yml --vault-password-file password.txt
```

in the Jenkinsfile.

## Steps to Run

## Authors

- [Ananthakrishna K](https://github.com/Ananthakrishna-K-13)
- [Prateek Rath](https://github.com/prateek-rath)
- [Mohit Naik](https://github.com/mohitiiitb)

