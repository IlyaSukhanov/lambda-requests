import os
from io import (
    BytesIO,
    StringIO,
)

from unittest import TestCase
from unittest.mock import patch
import requests

from lambda_requests import LambdaAdapter

LAMBDA_URL_PREFIX = "httplambda://flaskexp-test/"
HTTP_URL_PREFIX = "https://qrq3869e2e.execute-api.us-west-2.amazonaws.com/test/"
BINARY_PAYLOAD = bytes([0xde, 0xad, 0xbe, 0xef] * 100)
UNICODE_PAYLOAD = u"\u2620\U0001F42E" * 100


def _seek_reset_request(accessor, url_path, *args, **kwargs):
    if "files" in kwargs:
        for file_item in kwargs["files"]:
            kwargs["files"]["file"].seek(0)
    return accessor(url_path, *args, **kwargs)


class TestLambdaIntegration(TestCase):

    def setUp(self):
        self.http_accessor = requests.Session()
        self.lambda_accessor = requests.Session()
        self.lambda_accessor.mount('httplambda://', LambdaAdapter())

    def post_both(self, url_path, *args, **kwargs):
        return (
            _seek_reset_request(self.http_accessor.post, HTTP_URL_PREFIX + url_path, *args, **kwargs),
            _seek_reset_request(self.lambda_accessor.post, LAMBDA_URL_PREFIX + url_path, *args, **kwargs),
        )

    def get_both(self, url_path, *args, **kwargs):
        return (
            _seek_reset_request(self.lambda_accessor.get, LAMBDA_URL_PREFIX + url_path, *args, **kwargs),
            _seek_reset_request(self.http_accessor.get, HTTP_URL_PREFIX + url_path, *args, **kwargs),
        )

    def test_binary_file(self):
        """
        Send binary file via gateway and lambda invoke to echo service
        ensure we get same status code and content back.
        """
        with BytesIO(BINARY_PAYLOAD) as test_buffer:
            kwargs={"files":{'file': test_buffer}}
            responses = self.post_both("file", **kwargs)
            assert responses[0].status_code == responses[1].status_code
            assert responses[0].content == responses[1].content

    def test_unicode_file(self):
        """
        Send unicode file via gateway and lambda invoke to echo service
        ensure we get same status code and content back.
        """
        with StringIO(UNICODE_PAYLOAD) as test_buffer:
            kwargs={"files":{'file': test_buffer}}
            responses = self.post_both("file", **kwargs)
            assert responses[0].status_code == responses[1].status_code == 200
            assert responses[0].content == responses[1].content

    def test_path_parameter(self):
        responses = self.post_both("/test/foo")
        assert responses[0].status_code == responses[1].status_code == 200
        assert responses[0].json()["param"] == responses[1].json()["param"]

    def test_form_object(self):
        form_data = {"foo":"bar"}
        responses = self.post_both("/test/form", data=form_data)

        assert responses[0].status_code == responses[1].status_code == 200
        assert responses[0].json()["form"] == responses[1].json()["form"]

    def test_query_string(self):
        param_data = {"foo":"bar"}
        responses = self.get_both("/test/form", params=param_data)

        assert responses[0].status_code == responses[1].status_code == 200
        assert responses[0].json()["query_strings"] == responses[1].json()["query_strings"]

    #def test_custom_header(self):
    #def test_get
    #def test_head
    #def test_post
    #def test_patch
    #def test_post
    #def test_delete