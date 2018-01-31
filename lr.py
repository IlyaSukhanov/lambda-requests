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

    def _lambda_encode_request(self, request):
        """
        Convert a requests object to object mimicking API gateway
        simple proxy json object that can be handled by lambda
        http://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
        """
        try:
            body = request.body.decode('utf-8') if request.body else None
            base64_encoded = False
        except UnicodeDecodeError:
            body = base64.b64encode(request.body).decode('utf-8') if request.body else None
            base64_encoded = True
        return {
            "httpMethod": request.method,
            "path": request.path_url,
            "pathParameters": '',
            "queryStringParameters": '',
            "headers": dict(request.headers),
            "body": body,
            "isBase64Encoded": base64_encoded,
            "requestContext": {},
        }

    def _lambda_decode_reponse(self, lambda_response):
        """
        Convert json blob returned by lambda into one that requests
        clients are used to.
        """
        response = Response()
        response.status_code = lambda_response['statusCode']
        response.headers = lambda_response.get('headers', {})
        if lambda_response.get('isBase64Encoded', False):
            response.raw = BytesIO(base64.b64decode(lambda_response['body']))
        else:
            response.raw = BytesIO(lambda_response['body'].encode('utf-8'))
        return response

    def send(self, request, **kwargs):
        function_name = 'flaskexp-test'
        invocation_type = 'RequestResponse'
        log_type = 'Tail'
        payload = json.dumps(self._lambda_encode_request(request))
        logger.debug("Payload: %s", payload)

        client = boto3.client('lambda', region_name=REGION)
        lambda_response_raw = client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            LogType=log_type,
            Payload=payload,
        )

        # Unlike requests we read in whole object into memory as we need to
        # inspect some json fields, maybe there is a clever library that allows
        # this inspection without reading whole object
        lambda_response = json.loads(lambda_response_raw['Payload'].read().decode())
        return self._lambda_decode_reponse(lambda_response)


if __name__ == "__main__":
    s = requests.Session()
    s.mount('lambda://', LambdaAdapter())

    if False:
        resp = s.get('lambda://foo/test/foo')
        print("code: {}".format(resp.status_code))
        print("headers: {}".format(resp.headers))
        #print("body: {}".format(resp.body))
        #print("body: {}".format(hex_escape(resp.body)))
        #print(type(resp.body))
        print(resp.json())

    
    from tempfile import mkstemp
    #files = {'file': open('hypnotoad.svg', 'rb')}
    files = {'file': open('bender.png', 'rb')}
    if False:
        file_resp = s.post('lambda://foo/file', files=files)
        print("code: {}".format(file_resp.status_code))
        print("headers: {}".format(file_resp.headers))
        tempfile_descriptor, tempfile_name = mkstemp()
        tempfile = os.fdopen(tempfile_descriptor, mode='wb')
        print(dir(file_resp))
        tempfile.write(file_resp.content)
        tempfile.close()
        print("returned file be found in: {}".format(tempfile_name))


    if False:
        file_resp = requests.post('https://qrq3869e2e.execute-api.us-west-2.amazonaws.com/test/file', files=files)
        print("code: {}".format(file_resp.status_code))
        print("headers: {}".format(file_resp.headers))
        tempfile_descriptor, tempfile_name = mkstemp()
        tempfile = os.fdopen(tempfile_descriptor, mode='wb')
        print(dir(file_resp))
        tempfile.write(file_resp.content)
        tempfile.close()
        print("returned file be found in: {}".format(tempfile_name))
