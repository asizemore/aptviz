
FROM jupyter/datascience-notebook:python-3.8.6

RUN pip install plotly
RUN pip install -U kaleido
RUN python3 -m pip install --user --upgrade setuptools wheel



USER root
RUN apt-get update && apt-get install -y \
  libz-dev
  # libqt4-dev

USER jovyan

EXPOSE 8888
