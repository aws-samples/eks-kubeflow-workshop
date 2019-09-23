
> Note: In v0.6.2 kubeflow release, there's a profile kubeflow-anonymous created by default in the installation and you can skip this post setup. We suggest you use `kubeflow-anonymous` as default namespace for labs. If you'd like to create your own profile, please follow following steps.


## Create a user profile

Note: change `jiaxin` to your username.

```yaml
apiVersion: kubeflow.org/v1alpha1
kind: Profile
metadata:
  name: jiaxin
spec:
  owner:
    kind: User
    name: jiaxin
```

```
kubectl apply -f profile.yaml
```

## Grant your notebook service account access to entire namespace

Note: change `jiaxin` to your username.

```
kind: Role
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  namespace: jiaxin
  name: notebook-access
rules:
- apiGroups: ["*"] # "" indicates the core API group
  resources: ["*"]
  verbs: ["*"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: notebook-access-binding
  namespace: jiaxin
subjects:
- kind: ServiceAccount
  name: default-editor
  namespace: jiaxin
roleRef:
  kind: Role
  name: notebook-access
  apiGroup: rbac.authorization.k8s.io
```