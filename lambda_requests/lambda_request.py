import base64
import json
import os
import logging
from io import BytesIO
from urllib.parse import urlparse, parse_qs

import boto3
from requests.adapters import BaseAdapter
from requests.adapters import Response

logger = logging.getLogger(__name__)


def _lambda_query_string(url):
    return {
        key: value[0]
        for key, value
        in parse_qs(urlparse(url).query).items()
    }


class LambdaAdapter(BaseAdapter):
    def __init__(self, region=None):
        self.region = region or os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
        super(LambdaAdapter, self).__init__()

    def _lambda_encode_request(self, request):
        """
        Convert a requests object to object mimicking API gateway
        simple proxy json object that can be handled by lambda
        http://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
        """
        try:
            if not request.body:
                body = None
            elif isinstance(request.body, str):
                body = request.body
            else:
                body = request.body.decode('utf-8')
            base64_encoded = False
        except UnicodeDecodeError:
            body = base64.b64encode(request.body).decode('utf-8') if request.body else None
            base64_encoded = True
        return {
            "httpMethod": request.method,
            "path": urlparse(request.path_url).path,
            "pathParameters": '',
            "queryStringParameters": _lambda_query_string(request.url),
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
        if "body" in lambda_response:
            if lambda_response.get('isBase64Encoded', False):
                response.raw = BytesIO(base64.b64decode(lambda_response['body']))
            else:
                response.raw = BytesIO(lambda_response['body'].encode('utf-8'))
        return response

    def send(self, request, **kwargs):
        function_name = urlparse(request.url).hostname
        invocation_type = 'RequestResponse'
        log_type = 'Tail'
        raw_payload = self._lambda_encode_request(request)
        json_payload = json.dumps(raw_payload)
        logger.debug("Payload: %s", json_payload)

        client = boto3.client('lambda', region_name=self.region)
        lambda_response_raw = client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            LogType=log_type,
            Payload=json_payload,
        )

        # Unlike requests we read in whole object into memory as we need to
        # inspect some JSON fields, maybe there is a clever library that allows
        # this inspection without reading whole object
        lambda_response = json.loads(lambda_response_raw['Payload'].read().decode())
        return self._lambda_decode_reponse(lambda_response)
