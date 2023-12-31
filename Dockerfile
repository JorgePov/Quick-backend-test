FROM python:3.9-alpine

RUN apk add --update --no-cache --virtual .tmp-build-deps \
gcc libc-dev && apk add libffi-dev

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG PROJ_DIR=/api

RUN mkdir -p ${PROJ_DIR}

COPY . ${PROJ_DIR}

WORKDIR ${PROJ_DIR}

RUN pip3 install -r requirements.txt

RUN ["chmod", "+x", "./entrypoint.sh"]

ENTRYPOINT [ "sh", "./entrypoint.sh" ]
