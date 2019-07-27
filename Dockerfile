FROM python:3.6-stretch
USER root
ENV AIRFLOW__CORE__LOAD_EXAMPLES False
ENV AIRFLOW__CORE__DAGS_FOLDER /opt/src/main/python/dags
ENV AIRFLOW__CORE__PLUGINS_FOLDER /opt/src/main/python/plugins
ENV AIRFLOW__REST_API_PLUGIN__LOG_LOADING True
ENV AIRFLOW__REST_API_PLUGIN__FILTER_LOADING_MESSAGES_IN_CLI_RESPONSE True
ENV AIRFLOW__REST_API_PLUGIN__REST_API_PLUGIN_HTTP_TOKEN_HEADER_NAME rest_api_plugin_http_token
ENV AIRFLOW__REST_API_PLUGIN__REST_API_PLUGIN_EXPECTED_HTTP_TOKEN None

ENV AIRFLOW_HOME /usr/local/airflow

WORKDIR /opt

COPY build.py .
COPY src/unittest/python/resources/variables.json /usr/local/airflow/variables.json
COPY src/unittest/python/resources/connections.sh /usr/local/airflow/connections.sh

RUN pip install -U pip && \
  pip install pybuilder && \
  pyb install_dependencies && \
  airflow initdb && \
  airflow variables -i /usr/local/airflow/variable.json && \
  sh /usr/local/airflow/connections.sh

  RUN rm -f /opt/build.py
  RUN rm -f /usr/local/airflow/variables.json
  RUN rm -f /usr/local/airflow/connections.sh