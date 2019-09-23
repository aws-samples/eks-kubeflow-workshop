### Known issues

Can not find experiments in frontend if namespace is not kubeflow
https://github.com/kubeflow/katib/issues/774

If you submit experiment job in notebook directly, it will use same namespace `kubeflow-anonymous` but it won't show in the UI so we recommend you copy yaml files and change `namespace` to `kubeflow` to make visualization available.