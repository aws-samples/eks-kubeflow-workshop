This guidance shows how to uninstall Kubeflow and EKS cluster.

## Uninstall Kubeflow on exisiting EKS cluster.

Please follow [step](https://www.kubeflow.org/docs/aws/deploy/uninstall-kubeflow/) here to uninstall kubeflow.

## Delete EKS cluster

```
eksctl delete cluster -f cluster.yaml
```