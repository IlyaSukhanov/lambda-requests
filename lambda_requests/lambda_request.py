import logging
import os
from http import HTTPStatus

import boto3
import requests
from lambda_invoke import LambdaSimpleProxy
from requests.adapters import BaseAdapter
from requests.models import Response
from requests.utils import get_encoding_from_headers

logger = logging.getLogger(__name__)

STATUS_CODES_TO_REASON_PHRASES = {status.value: status.name for status in HTTPStatus}
DEFAULT_SCHEME = "http+lambda://"


class Session(requests.Session):
    def __init__(self, url_scheme=None, region=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adapter = LambdaAdapter(region=region)
        self.mount(url_scheme or DEFAULT_SCHEME, self.adapter)

    def __enter__(self):
        self.adapter.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        self.adapter.__exit__(*args, **kwargs)


class LambdaAdapter(BaseAdapter):
    def __init__(self, region=None):
        self.region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self._lambda_client = None
        super(LambdaAdapter, self).__init__()

    def __enter__(self):
        return self

    def __exit__(self, *_, **__):
        pass

    @property
    def lambda_client(self):
        if not self._lambda_client:
            self._lambda_client = boto3.client("lambda", region_name=self.region)
        return self._lambda_client

    def send(self, request, **kwargs):
        invoke = LambdaSimpleProxy(
            self.region,
            request.method,
            request.url,
            dict(request.headers),
            request.body,
        )

        lambda_response = invoke.send(self.lambda_client)
        encoding = get_encoding_from_headers(lambda_response.headers)

        response = Response()
        response.status_code = lambda_response.status_code
        response.reason = STATUS_CODES_TO_REASON_PHRASES[lambda_response.status_code]
        response.headers = lambda_response.headers
        response.encoding = encoding
        response.raw = lambda_response.body_stream
        return response
