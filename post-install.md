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

## Create a notebook




## Clone workshop repository into your workspace

Open a terminal in Jupyter notebook,

```
git clone https://github.com/Jeffwan/kubeflow-eks-workshop.git
```