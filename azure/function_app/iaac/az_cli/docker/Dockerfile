# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.10-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.10

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY requirements.txt /

# === Ubuntu/Debian Region ===
# expects certificates to be under the <PROJECT_ROOT>/certs directory
RUN cat /etc/os-release
RUN mkdir -p /tmp/certs
COPY "certs/*.crt" /tmp/certs
COPY "certs/*.pem" /tmp/certs
RUN ls -la /tmp/certs
RUN apt-get update
RUN apt-get install ca-certificates -y
RUN cp /tmp/certs/*.crt /usr/local/share/ca-certificates
RUN cp /tmp/certs/*.pem /usr/local/share/ca-certificates
RUN ls -la /usr/local/share/ca-certificates
RUN update-ca-certificates


# === Example fix for pip SSL error === 
# For the initial upgrade we implicitly trust the pip upgrade provider, but after that, next each install utilises SSL
RUN export AZURE_CLI_DISABLE_CONNECTION_VERIFICATION=1
RUN pip install --trusted-host pypi.org --upgrade pip 
RUN pip install -r /requirements.txt --use-feature=truststore
# TODO: impove fix as SSL verification is disabled for Pip upgrade
# IDEAS: 
# IDEA 1) find way to trust certificate 
# RUN echo "[global]" >> /etc/pip.conf
# RUN echo "cert = /usr/local/share/ca-certificates/<FILENAME>.crt" >> etc/pip.conf
# RUN export REQUESTS_CA_BUNDLE=/usr/local/share/ca-certificates/<FILENAME>.pem
# RUN echo $REQUESTS_CA_BUNDLE
# RUN pip3 --cert /usr/local/share/ca-certificates/<FILENAME>.pem install -r /requirements.txt
# IDEA 2) use newer base image

COPY . /home/site/wwwroot