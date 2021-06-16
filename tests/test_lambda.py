import base64
import json
from io import BytesIO, StringIO

import requests

from lambda_requests import LambdaAdapter
from tests.base import (
    BINARY_PAYLOAD,
    LAMBDA_URL_PREFIX,
    UNICODE_PAYLOAD,
    PatcherBase,
)


class TestLambda(PatcherBase):
    def setUp(self):
        self.http_accessor = requests.Session()
        self.lambda_accessor = requests.Session()
        self.lambda_accessor.mount("httplambda://", LambdaAdapter())
        self.boto3 = self.add_patcher("lambda_requests.lambda_request.boto3")

    def extract_sent_payload(self, key):
        return json.loads(self.boto3.client().invoke.call_args[1]["Payload"])[key]

    def post(self, url_path, *args, **kwargs):
        return self.lambda_accessor.post(LAMBDA_URL_PREFIX + url_path, *args, **kwargs)

    def get(self, url_path, *args, **kwargs):
        return self.lambda_accessor.get(LAMBDA_URL_PREFIX + url_path, *args, **kwargs)

    def set_response_payload(self, payload):
        self.boto3.client().invoke().__getitem__().read.return_value = payload

    def test_binary_file(self):
        self.set_response_payload(
            b'{"body": "3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+796tvu/erb7v3q2+7w==", "isBase64Encoded": "true", "statusCode": 200, "headers": {"Content-Type": "application/octet-stream", "Cache-Control": "public, max-age=43200", "Expires": "Tue, 15 Jun 2021 13:50:28 GMT", "X-Request-ID": ""}}'  # noqa: E501
        )

        with BytesIO(BINARY_PAYLOAD) as test_buffer:
            kwargs = {"files": {"file": test_buffer}}
            response = self.post("/file", **kwargs)
            assert self.extract_sent_payload("path") == "/file"
            assert self.extract_sent_payload("httpMethod") == "POST"
            assert b"filename" in base64.b64decode((self.extract_sent_payload("body")))
            assert response.status_code == 200
            assert (
                response.content
                == b"\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef\xde\xad\xbe\xef"  # noqa: E501
            )

    def test_unicode_file(self):
        self.set_response_payload(
            b'{"body": "4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+QruKYoPCfkK7imKDwn5Cu4pig8J+Qrg==", "isBase64Encoded": "true", "statusCode": 200, "headers": {"Content-Type": "application/octet-stream", "Cache-Control": "public, max-age=43200", "Expires": "Tue, 15 Jun 2021 14:02:28 GMT", "X-Request-ID": ""}}'  # noqa: E501
        )

        with StringIO(UNICODE_PAYLOAD) as test_buffer:
            kwargs = {"files": {"file": test_buffer}}
            response = self.post("/file", **kwargs)
            assert response.status_code == 200
            assert self.extract_sent_payload("path") == "/file"
            assert self.extract_sent_payload("httpMethod") == "POST"
            assert "filename" in (self.extract_sent_payload("body"))
            assert (
                response.content
                == b"\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae\xe2\x98\xa0\xf0\x9f\x90\xae"  # noqa: E501
            )

    def test_path_parameter(self):
        self.set_response_payload(
            b'{"body": "ewogICJmb3JtIjoge30sIAogICJoZWFkZXJzIjogIlVzZXItQWdlbnQ6IHB5dGhvbi1yZXF1ZXN0cy8yLjI1LjFcclxuQWNjZXB0LUVuY29kaW5nOiBnemlwLCBkZWZsYXRlXHJcbkFjY2VwdDogKi8qXHJcbkNvbm5lY3Rpb246IGtlZXAtYWxpdmVcclxuXHJcbiIsIAogICJwYXJhbSI6ICJmb28iLCAKICAicXVlcnlfc3RyaW5ncyI6IHt9Cn0K", "isBase64Encoded": "true", "statusCode": 200, "headers": {"Content-Type": "application/json", "X-Request-ID": "", "Content-Length": "195"}}'  # noqa: E501
        )
        response = self.get("/test/foo")
        assert self.extract_sent_payload("path") == "/test/foo"
        assert self.extract_sent_payload("httpMethod") == "GET"
        assert response.status_code == 200
        assert response.json()["param"] == "foo"

    def test_form_object(self):
        self.set_response_payload(
            b'{"body": "ewogICJmb3JtIjogewogICAgImZvbyI6ICJiYXIiCiAgfSwgCiAgImhlYWRlcnMiOiAiQ29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi94LXd3dy1mb3JtLXVybGVuY29kZWRcclxuQ29udGVudC1MZW5ndGg6IDdcclxuVXNlci1BZ2VudDogcHl0aG9uLXJlcXVlc3RzLzIuMjUuMVxyXG5BY2NlcHQtRW5jb2Rpbmc6IGd6aXAsIGRlZmxhdGVcclxuQWNjZXB0OiAqLypcclxuQ29ubmVjdGlvbjoga2VlcC1hbGl2ZVxyXG5cclxuIiwgCiAgInBhcmFtIjogImZvcm0iLCAKICAicXVlcnlfc3RyaW5ncyI6IHt9Cn0K", "isBase64Encoded": "true", "statusCode": 200, "headers": {"Content-Type": "application/json", "X-Request-ID": "", "Content-Length": "288"}}'  # noqa: E501
        )
        form_data = {"foo": "bar"}
        response = self.post("/test/form", data=form_data)
        assert self.extract_sent_payload("path") == "/test/form"
        assert self.extract_sent_payload("httpMethod") == "POST"
        assert self.extract_sent_payload("body") == "foo=bar"
        assert response.status_code == 200
        assert response.json()["form"] == form_data

    def test_query_string(self):
        self.set_response_payload(
            b'{"body": "ewogICJmb3JtIjoge30sIAogICJoZWFkZXJzIjogIlVzZXItQWdlbnQ6IHB5dGhvbi1yZXF1ZXN0cy8yLjI1LjFcclxuQWNjZXB0LUVuY29kaW5nOiBnemlwLCBkZWZsYXRlXHJcbkFjY2VwdDogKi8qXHJcbkNvbm5lY3Rpb246IGtlZXAtYWxpdmVcclxuXHJcbiIsIAogICJwYXJhbSI6ICJmb3JtIiwgCiAgInF1ZXJ5X3N0cmluZ3MiOiB7CiAgICAiZm9vIjogImJhciIKICB9Cn0K", "isBase64Encoded": "true", "statusCode": 200, "headers": {"Content-Type": "application/json", "X-Request-ID": "", "Content-Length": "216"}}'  # noqa: E501
        )
        param_data = {"foo": "bar"}
        response = self.get("/test/form", params=param_data)
        assert self.extract_sent_payload("path") == "/test/form"
        assert self.extract_sent_payload("httpMethod") == "GET"
        assert self.extract_sent_payload("queryStringParameters") == param_data
        assert response.status_code == 200
        assert response.json()["query_strings"] == param_data

    def test_custom_header(self):
        self.set_response_payload(
            b'{"body": "ewogICJmb3JtIjoge30sIAogICJoZWFkZXJzIjogIlVzZXItQWdlbnQ6IHB5dGhvbi1yZXF1ZXN0cy8yLjI1LjFcclxuQWNjZXB0LUVuY29kaW5nOiBnemlwLCBkZWZsYXRlXHJcbkFjY2VwdDogKi8qXHJcbkNvbm5lY3Rpb246IGtlZXAtYWxpdmVcclxuRm9vOiBiYXJcclxuXHJcbiIsIAogICJwYXJhbSI6ICJmb3JtIiwgCiAgInF1ZXJ5X3N0cmluZ3MiOiB7fQp9Cg==", "isBase64Encoded": "true", "statusCode": 200, "headers": {"Content-Type": "application/json", "X-Request-ID": "", "Content-Length": "208"}}'  # noqa: E501
        )
        header_data = {"foo": "bar"}
        response = self.get("/test/form", headers=header_data)
        assert self.extract_sent_payload("path") == "/test/form"
        assert self.extract_sent_payload("httpMethod") == "GET"
        assert self.extract_sent_payload("headers")["foo"] == "bar"
        assert response.status_code == 200
        assert response.json()["headers"].lower().find("foo") > 0
        assert response.json()["headers"].lower().find("bar") > 0

    def test_lambda_exception(self):
        self.set_response_payload(
            b'{"errorMessage": "Unable to import module \'service\': No module named \'foobarbaz\'", "errorType": "Runtime.ImportModuleError", "stackTrace": [] }'  # noqa: E501
        )
        response = self.get("/lambda_exception")
        assert response.status_code == 502
        assert (
            response.content
            == b"Unable to import module 'service': No module named 'foobarbaz'"
        )
