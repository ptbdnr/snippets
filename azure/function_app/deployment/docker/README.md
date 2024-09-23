# Deploy code to Azure Function App


## Requirements

* Azure subscription
* Azure CLI: to sing-in to the Azure account
* Azure Functions Core Tools: to initialise a project
* Docker account (Docker ID) and Docker running on local computer: to build a docker image

```shell
# Azure CLI expected version: 2.61 or higher
az --version
# Azure Functions Core Tools expected version: 4.x or higher
func upgrade
func --version
# Docker expected version 27.x or higher
docker --version
```

## Create a project

ref: https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python


1. Create a local project 

Optionally add `--docker` to create a Dockerfile.

```shell
func init \ 
    --worker-runtime python \ 
    --model V2
```

3. Create a Function App locally

In this example the Function App can be triggered by a HTTP request and has a route called `FUNCTION_NAME` (e.g. httpTriggerName)

```shell
func new \ 
    --template "Http Trigger" \ 
    --name $FUNCTION_NAME
```

4. Add a default Dockerfile to an existing project

ref: https://learn.microsoft.com/en-us/azure/azure-functions/functions-core-tools-reference?tabs=v2#func-init

```shell
func init --docker-only
```

5. Create and activate a virtual environment

```shell
python -m venv .venv
source .venv/bin/activate
```


## Start the Functions runtime and test locally


1. Start the functions runtime
```shell
func start
```

2. Run a local function (in a new terminal)

endpoint pattern `http://localhost:<PORT>/api/<FUNCTION_NAME>`

```shell
curl --get http://localhost:7071/api/$FUNCTION_NAME?name=Joe%20Doe
```

or

```bash
curl --request POST http://localhost:7071/api/$FUNCTION_NAME --data '{"name":"Joe Doe"}'
```

3. Build Docker image locally and verify by running it locally. 

`DOCKER_ID` is the Docker Hub account ID, `IMAGE_NAME` is an arbitrary project name, `TAG` is an arbitrary tag (e.g. v1.0.0). Note the dot `.` indicating that the path to the Dockerfile is the present working working directory.

NB: Azure CLI uses the requests library which looks for the environment variable `REQUESTS_CA_BUNDLE`. ensure this is pointing to the location of our '.pem' certificate file (if applicable): `export REQUESTS_CA_BUNDLE=/PATH/TO/FILE.pem`

NB2: alternative is to upgrade pip and use-feature=truststore

```shell
RUN pip install --trusted-host pypi.org --upgrade pip 
#Non-Ideal fix as SSL verification is disabled for Pip upgrade
#Either find way to trust certificate - or use more up to date base image
RUN pip install -r /requirements.txt --use-feature=truststore
```

```shell
docker build --progress=plain --no-cache --tag $DOCKER_ID/$IMAGE_NAME:$TAG .
# or build directly on Azure: az acr build --registry $REGISTRY_NAME --image $LOGIN_SERVER/$PATH/$IMAGE_NAME:$TAG .
docker run -p 8080:80 -it $DOCKER_ID/$IMAGE_NAME:$TAG
```

## Deploy project files directly to existing Function App using zip deployment

ref: https://learn.microsoft.com/en-us/azure/azure-functions/functions-core-tools-reference?tabs=v2#func-azure-functionapp-publish

```shell
func azure functionapp publish $APP_NAME
```

## Deploy Docker image to Container Registry that updates the Azure Function App

ref: https://learn.microsoft.com/en-us/azure/azure-functions/functions-deploy-container-apps?tabs=acr%2Cbash&pivots=programming-language-python

ref: https://learn.microsoft.com/en-us/cli/azure/acr?view=azure-cli-latest#az-acr-login

```shell
# sign int ot the container registry instance. alternative: docker login $REGISTRY_NAME.azurecr.io
az acr login --name $REGISTRY_NAME
# tag the Docker image where `DOCKER_ID` is your Docker account Id, `LOGIN_SERVER` is the name of the registry login server (eg. $REGISTRY_NAME.azurecr.io), so that it can be pushed to the private registry. IMAGE_NAME may contain '/'. `TAG` is optional, default value is `latest`
docker tag $DOCKER_ID/$IMAGE_NAME:$TAG $LOGIN_SERVER/$IMAGE_NAME:$TAG
# pus the image to the registry instance
docker push $LOGIN_SERVER/$IMAGE_NAME:$TAG
```

Verify that the image is in the container repository by pulling it

```shell
docker pull $LOGIN_SERVER/$IMAGE_NAME:$TAG
```