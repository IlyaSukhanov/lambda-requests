===============================
Lambda-Requests
===============================


.. image:: https://img.shields.io/pypi/v/lambda_requests.svg
        :target: https://pypi.python.org/pypi/lambda_requests


Lambda-requests use the well familiar requests library to access your HTTP
enabled AWS Lambda functions.

Quick start
------------

Installation
````````````

.. code-block:: shell

    pip intall lambda_requests

Usage
`````

.. code-block:: python

    >>> import requests
    >>> from lambda_requests import LambdaAdapter
    >>> la = requests.Session()
    >>> la.mount("httplambda://", LambdaAdapter())
    >>> la.get("httplambda://flaskexp-test/test/foo")
    <Response [200]>

In short mount `LambdaAdapter` to requests session then access your lambdas by
using url of this format `httplambda://{name-of-lambda-function}/...` then use
`requests`_ as you normally would; get, post, query strings, form data ... etc.

Lambda authorization is configured via `boto3`_, and can be set up using
`environment variables`_ or a `configuration file`_. Configuration file is
recommended. Example credential file ~/.aws/credentials:

.. code-block:: ini

    [default]
    aws_access_key_id =  XXXXXXXXXXXXXXXXXXXX
    aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Similar to authorization, region can be configured either via the `environment
variable`_ `AWS_DEFAULT_REGION`, `configuration file`_. Region can also be set
on initialization of LambdaAdapter(region:'us-west-2'). Example configuration
file ~/.aws/config:

.. code-block:: ini

    [profile default]
    region = us-west-2

The lambdas must support `proxy integration`_, which is used commonly by frameworks
such as `Zappa`_, `Mangum`_.



.. _`boto3`: https://boto3.readthedocs.io/en/latest/
.. _`requests`: http://docs.python-requests.org/en/master/
.. _`proxy integration`: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
.. _`Zappa`: https://github.com/zappa/Zappa
.. _`Mangum`: https://mangum.io/
.. _`environment variables`: http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables
.. _`configuration file`: http://boto3.readthedocs.io/en/latest/guide/configuration.html#shared-credentials-file
.. _`environment variable`: http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variable-configuration
.. _`configuration file option`: http://boto3.readthedocs.io/en/latest/guide/configuration.html#configuration-file

Why
---

In using REST microservice architecture it is important to be able to
conveniently make calls from one service to another. To use this pattern
in AWS serverless ecosphere along with Lambda one is practically forced
to stand up an API Gateway in front of the lambda. This has several distinct
disadvantages, all mostly along the lines of security.

* API Gateway publicly exposes endpoints
* API Gateway uses own authentication / authorization schema. While Lambda
  already supplies us with IAM.
* Extra dependencies in call chain. While availability is high, latency may
  still be of concern.

Over all, to reduce exposure of private sub-services, re-use IAM authentication
/ authorization and reduce latency.

How does its work
-----------------

Simple, we register a new protocol name with requests and use a lambda
specific `transport adapter`_ which translates a requests request
to `lambda invoke`_ compatible with AWS API Gateway simple proxy format.

.. _`transport adapter`: http://docs.python-requests.org/en/master/user/advanced/#transport-adapters
.. _`lambda invoke`: http://boto3.readthedocs.io/en/latest/reference/services/lambda.html#Lambda.Client.invoke
