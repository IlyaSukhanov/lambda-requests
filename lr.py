import base64
import json
import os
import logging
from io import BytesIO

import boto3
import requests
from requests.adapters import BaseAdapter
from requests.adapters import Response

logger = logging.getLogger(__name__)
REGION = os.environ.get('AWS_DEFAULT_REGION', 'us-west-2')

import string
printable = string.ascii_letters + string.digits + string.punctuation + ' '
def hex_escape(s):
    return ''.join(c if c in printable else r'\x{0:02x}'.format(ord(c)) for c in s)

class LambdaAdapter(BaseAdapter):
    def __init__(self):
        super(LambdaAdapter, self).__init__()

    def send(self, request, **kwargs):
        print(kwargs)
        function_name = 'flaskexp-test'
        invocation_type = 'RequestResponse'
        log_type = 'Tail'
        path_parameters = ''
        qs_parameters = ''
        print(request.path_url)
        print(dict(request.headers))
        print(request.headers.items())
        # http://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
        payload = {
            "httpMethod": request.method,
            "path": request.path_url,
            "pathParameters": path_parameters,
            "queryStringParameters": qs_parameters,
            "headers": dict(request.headers),
            "body": request.body,
            "requestContext": {}
        }

        client = boto3.client('lambda', region_name=REGION)
        lambda_response_raw = client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            LogType=log_type,
            Payload=json.dumps(payload)
        )
        lambda_response = json.loads(lambda_response_raw['Payload'].read())
        logger.debug("Payload: %s", payload)
        print(lambda_response)
        response = Response()
        response.status_code = lambda_response['statusCode']
        response.headers = lambda_response['headers']
        response.raw = BytesIO(lambda_response['body'].encode('utf-8'))
        return response


if __name__ == "__main__":
    s = requests.Session()
    s.mount('lambda://', LambdaAdapter())
    resp = s.get('lambda://foo/test/foo')
    print("code: {}".format(resp.status_code))
    print("headers: {}".format(resp.headers))
    #print("body: {}".format(resp.body))
    #print("body: {}".format(hex_escape(resp.body)))
    #print(type(resp.body))
    print(resp.json())
