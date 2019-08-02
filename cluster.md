This guidance shows how to run an AWS EKS cluster for kubeflow workshop. Consider the real world use case, we will create the EKS cluster in a cost effective way using Spot instance which can save up to 90% comparing to On-Demand price. 

# EKS Optimized AMI image with GPU support
# eksctl CLI Tools


## EKS Cluster
First we need to create a Kubernetes cluster that consists from mixed nodes, CPU nodes for management and generic Kubernetes workload and acclerate GPU nodes to run GPU intensive tasks, like machine learning training, High Performance Computing(HPC) jobs. 

These node groups should be able to scale on demand (scale out and scale in) for generic nodes, and from 0 to required number and back to 0 for expensive GPU instances. More than that, in order to do it in cost effective way, we are going to use Amazon EC2 Spot Instances both for generic nodes and GPU nodes.


## The Workflow

### Create EKS Cluster

In this workshop, we highly recommend you to create an EKS cluster using eksctl CLI tool. While, you can also create AWS EKS cluster, using AWS EKS CLI, CloudFormation or Terraform, AWS CDK. 

It is possible to pass all parameters to the tool as CLI flags or configuration file. Using configuration file makes process more repeatable and automation friendly.

```
eksctl create cluster -f cluster.yaml
```

What would give to you 

* 
* Scale from 0
* Auto configure policy for IAM, ALB, Storage, etc.


### Install Kubeflow
The kfctl golang client is CLI tool to install kubeflow. Please download current version v0.6.1 here based on your platform. Choose binary based on your platform. 

### Create aws secret in the cluster

Reference: https://alexei-led.github.io/post/eks_gpu_spot/
