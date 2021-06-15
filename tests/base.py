from unittest.mock import DEFAULT, patch
from unittest import TestCase


LAMBDA_URL_PREFIX = "httplambda://flaskexp-test"
HTTP_URL_PREFIX = "https://qrq3869e2e.execute-api.us-west-2.amazonaws.com/test/"
BINARY_PAYLOAD = bytes([0xde, 0xad, 0xbe, 0xef] * 100)
UNICODE_PAYLOAD = u"\u2620\U0001F42E" * 100

class PatcherBase(TestCase):
    def add_patcher(self, target, new=DEFAULT):
        target_patch = patch(target, new)
        self.addCleanup(target_patch.stop)
        return target_patch.start()
