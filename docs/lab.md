## Create a notebook

Click `Notebook Servers` -> `New Server` to cerate a notebook. We added awscli and docker client support which needed for fairing experiment. We recommend you to use `seedjeffwan/tensorflow-1.13.1-notebook-cpu:awscli-v2` as a custom image to provision your notebook temprorily. I am working on upstream patch to make it as default package in upstream images.

## Clone workshop repository into your workspace

Open a terminal in Jupyter notebook,
```
git clone https://github.com/aws-samples/eks-kubeflow-workshop.git
```