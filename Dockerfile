FROM python:alpine

# The version of wdc contained in the image. Defaults to latest
ARG VERSION=latest

# Set image labels
LABEL "wdc.version"=$VERSION
LABEL "maintaner"="dejan@fajfar.com"


WORKDIR /wdc

COPY dist/*.whl .
COPY tests/integration/*.* .

RUN pip install *.whl
