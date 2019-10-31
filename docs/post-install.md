
> Note: In v0.7.0 kubeflow release, there's a profile `anonymous` created by default in the installation and you can skip this post setup. We suggest you use `anonymous` as default namespace for labs. If you'd like to create your own profile, please follow following steps.


## Grant your notebook service account access to entire namespace

In order to submit arbitrary custom job types, we need to grant `anonymous` permissions.

```
kind: Role
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  namespace: anonymous
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
  namespace: anonymous
subjects:
- kind: ServiceAccount
  name: default-editor
  namespace: anonymous
roleRef:
  kind: Role
  name: notebook-access
  apiGroup: rbac.authorization.k8s.io
```

Save the file and `kubectl apply -f bindings.yaml`

## Create a new user profile

Note: change `jiaxin` to your username.

```yaml
apiVersion: kubeflow.org/v1beta1
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

Beside profile, you need to create Role and RoleBindings as well for user `jiaxin`. Replace `anonymous` with `jiaxin`