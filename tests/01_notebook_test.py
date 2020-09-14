import papermill as pm

pm.execute_notebook(
   'notebooks/01_Jupyter_Notebook/01_01_Notebook_Development.ipynb',
   '/tmp/eks-kubeflow/workshop/test_output/01_Notebook_Development.ipynb'
   )

