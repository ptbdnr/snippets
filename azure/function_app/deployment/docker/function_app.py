import azure.functions as func
import logging

app = func.FunctionApp()
VERSION = "1.10.0"


@app.route(route="httpTriggerName", auth_level=func.AuthLevel.ANONYMOUS)
def httpTriggerName(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"({VERSION}) Hello, {name}.")
    else:
        return func.HttpResponse(
             (f"({VERSION}) "
              + "Pass a 'name' in the query string"
              + "or in the request body."),
             status_code=200
        )
