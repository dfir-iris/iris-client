# Python client

`dfir_iris_client` offers a Python interface to communicate with IRIS.

It relies exclusively on the API, which means output of the methods are the same as specified in the API reference.

## Versions
The Python client version follows the API versions (until the patch level). Meaning for API v2.0.1, one need to install `dfir_iris_client-2.0.1`. 
Please refer to the [documentation](https://dfir-iris.github.io/operations/api/#references) to check which version applies to your IRIS instance. 

## Install 
IRIS Client is now part of PyPI. You can simply install it with : 
```
pip3 install dfir-iris-client
```

## Build
To build a wheel from the sources:

1. `pip3 install wheel`
2. `python setup.py bdist_wheel`
3. `pip3 install dist/XXX.whl`


## How to run tests locally
The following commands create a local envrionment to run the python client test against a IRIS instance created with docker compose.
It requires [pytest](https://docs.pytest.org/en/stable/) for running the tests.

1. Clone [iris-web](https://github.com/dfir-iris/iris-web) and [iris-client](https://github.com/dfir-iris/iris-client)
2. Copy the test .env over: `cp iris-client/dfir_iris_client/tests/resources/.env iris-web/.env`
3. Start the IRIS instance `docker compose -f iris-web/docker-compose.dev.yml up -d`
4. Read the .env into the shell environment to access the token: `set -a &&  source iris-web/.env && set +a`
5. Run the tests: `pytest iris-client/dfir_iris_client/tests/`
6. Tear down and remove volumes: `docker compose -f iris-web/docker-compose.dev.yml down --volumes`

## Examples
Some examples are available [here](https://github.com/dfir-iris/iris-client/tree/master/examples).

## Documentation 
The documentation is available in the [IRIS documentation](https://docs.dfir-iris.org/python_client/).
