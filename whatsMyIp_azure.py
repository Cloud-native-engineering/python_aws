import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="myip")
def myip(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info(req.headers)
    for header_name, header_value in req.headers.items():
        logging.info(f"{header_name}: {header_value}")

    source_ip = req.headers.get('X-Forwarded-For')

    return func.HttpResponse(f"Source IP: {source_ip}", status_code=200)