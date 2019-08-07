FROM python:3.7.0

LABEL maintainer "Jiaxin Shan <shjiaxin@amazon.com>"

RUN pip install mlflow==1.0.0
RUN pip install boto3
RUN pip install awscli --upgrade --user

ENV AWS_MLFLOW_BUCKET aws_mlflow_bucket
ENV AWS_ACCESS_KEY_ID aws_access_key_id
ENV AWS_SECRET_ACCESS_KEY aws_secret_access_key

COPY run.sh /

ENTRYPOINT ["/run.sh"]

# docker build -t seedjeffwan/mlflow-tracking-server:1.0.0 .
# 1.0.0 is current mlflow version