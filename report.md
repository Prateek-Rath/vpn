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

![Architecture](arch.png)

### Containerization and Orchestration

### Monitoring

### Logging

### CI/CD

### Infrastructure

## Steps to Run

## Authors

- [Ananthakrishna K](https://github.com/Ananthakrishna-K-13)
- [Prateek Rath](https://github.com/prateek-rath)
- [Mohit Naik](https://github.com/mohitiiitb)

