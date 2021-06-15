from unittest import TestCase
from unittest.mock import DEFAULT, patch

LAMBDA_URL_PREFIX = "httplambda://flaskexp-test"
HTTP_URL_PREFIX = "https://qrq3869e2e.execute-api.us-west-2.amazonaws.com/test/"
BINARY_PAYLOAD = bytes([0xDE, 0xAD, 0xBE, 0xEF] * 100)
UNICODE_PAYLOAD = u"\u2620\U0001F42E" * 100


class PatcherBase(TestCase):
    def add_patcher(self, target, new=DEFAULT):
        target_patch = patch(target, new)
        self.addCleanup(target_patch.stop)
        return target_patch.start()
