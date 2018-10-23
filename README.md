[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

# secret-store-client-py 

>    🐳  Python client for Parity Secret Store.
>    [oceanprotocol.com](https://oceanprotocol.com)


[![Travis (.com)](https://img.shields.io/travis/com/oceanprotocol/secret-store-client-py.svg)](https://travis-ci.com/oceanprotocol/secret-store-client-py)
[![PyPI](https://img.shields.io/pypi/v/secret-store-client.svg)](https://pypi.org/project/secret-store-client/)


---

## Table of Contents

  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Quickstart](#quickstart)
  - [Environment variables](#environment-variables)
  - [Code style](#code-style)
  - [Testing](#testing)
  - [New Version](#new-version)
  - [License](#license)

---

## Features

- Encrypt and publish encrypted documents to the Parity Secret Store.
- Fetch and decrypt the documents from the Parity Secret Store, if permissions are given.

## Prerequisites

- A URL of a Secret Store node that accepts requests.
- A supported version of Python. For details, see `setup.py`.
- A JSON-RPC URL of the [Parity EVM client](https://github.com/paritytech/parity-ethereum). It is strongly recommended to run the client locally.

- A publisher Ethereum account, for publishing documents.
- A consumer Ethreum account, for consuming documents.

## Quickstart

#### Instantiate a publisher

```
from secret_store_client import Client

secret_store_url = 'http://localhost:8010'
parity_client_url = 'http://localhost:8545'
publisher_address = '0xc8307e6fbe40e97061a7b9f88b98df9249e4cefd'
publisher_password = 'publisherpwd'

publisher = Client(secret_store_url, parity_client_url,
                   publisher_address, publisher_password)
```

#### Publish a document

```
import hashlib

document = 'mySecretDocument'
# we need a 256 bit hash
document_id = hashlib.sha256(document.encode()).hexdigest()

encrypted = publisher.publish_document(document_id, document)
```

By default, if there are multiple Secret Store nodes, all nodes are required to participate in the encryption process. You can allow one or more nodes to not participate by passing a custom `threshold` parameter:

```
encrypted = publisher.publish_document(document_id, document, threshold=1)
```

You can find some guidance on how to choose a threshold [here](https://wiki.parity.io/Secret-Store#server-key-generation-session).

#### Instantiate a consumer

```
from secret_store_client import Client

secret_store_url = 'http://localhost:8010'
parity_client_url = 'http://localhost:8545'
consumer_address = '0xe887f790103a108e9c500cf167bfef019f5f41e0'
consumer_password = 'consumerpwd'

consumer = Client(secret_store_url, parity_client_url,
                  consumer_address, consumer_password)
```

#### Decrypt the document

```
decrypted = consumer.decrypt_document(document_id, encrypted)

assert 'mySecretDocument' == decrypted
```

## Development

The Secret Store setup instructions in this section is a simplification of the instructions presented [here](https://wiki.parity.io/Secret-Store-Tutorial-1.html).

#### Download and compile the Parity Ethereum client

Follow these [instructions](https://wiki.parity.io/Secret-Store-Tutorial-1.html#1-enable-the-secret-store-feature-of-parity).

Put the `./target/release/parity` binary somewhere on your PATH.

#### Configure a publisher node

Make a copy of the user configuration template.

```
cp integration_tests/configs/users.template.toml integration_tests/configs/users.toml
```

Create an account.

```
parity --config integration_tests/configs/users.toml account new
```

It asks you for a password and outputs an address.


Now make a copy of the test configuration template.

```
cp integration_tests/configs/test_setup.template.conf integration_tests/configs/test_setup.conf
```

Insert your publisher password and address into the corresponding placeholders inside `test_setup.conf`.


#### Configure a consumer node

Repeat the steps from the previous section except for this time fill in consumer address and password in the configuration file.


#### Configure a Secret Store node

Make a copy of the Secret Store configuration template.

```
cp integration_tests/configs/secret_store.template.toml integration_tests/configs/secret_store.toml
```

Create an account.

```
parity --config integration_tests/configs/secret_store.toml account new
```

It asks you for a password and outputs an address.

Put your password into `integration_tests/configs/ss.pwd`. Put the account address into the corresponding place
inside `integration_tests/configs/secret_store.toml` and uncomment the `password =` line.

Run the Secret Store node.

```
parity --config integration_tests/configs/secret_store.toml
```

It outputs its public node URL.

```
...
Public node URL: enode://a67dd8d6ffbf81fdd98fdae6902c527c77de34bc6fc39ffa8767126ee71d73484f8f7f692c02f095682b2578e11af004ab68ba47d8a923a7b868a040d2f6d479@192.168.86.248:30301
```

Insert this URL into the `bootnodes` list of your `users.toml`.

#### Deploy the test permission contract

Install `truffle`:

```
npm -g install truffle@beta
```

Note the versions the process was tested with.
```
npm 6.4.1
node v9.11.2
Truffle v5.0.0-beta.1 (core: 5.0.0-beta.1)
Solidity v0.4.25 (solc-js)
```

Compile the contract.

```
truffle compile
```

Deploy the contract.

```
truffle migrate
```

It outputs "contract address". Copy it and insert as a value for `acl_contract` into `secret_store.toml`.

Relaunch the node for the change to take action.

#### Run the nodes

The steps above have to only be performed once. Every time you want to develop or test, just run the Secret Store node and the Parity Ethereum client.

Run the Secret Store node:

```
parity --config integration_tests/configs/secret_store.toml
```

Run the Parity Ethereum client:
```
parity --config integration_tests/configs/users.toml
```

#### Execute integration tests

Make sure the Secret Store node and the Parity Ethereum client are up and running, then execute:

```
python3 setup.py test
```

Automatic tests are setup via Travis, executing `tox`.
Our test use pytest framework.

## Code style

The information about code style in python is documented in this two links [python-developer-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-developer-guide.md)
and [python-style-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-style-guide.md).

### TLDR

```
pip install flake8
flake8 secret_store_client integration_tests tests
```

## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute the script using as first argument {major|minor|patch} to bump accordingly the version.

## License

```
Copyright 2018 Ocean Protocol Foundation Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
