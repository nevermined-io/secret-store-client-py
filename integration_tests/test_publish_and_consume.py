import hashlib
import os
import uuid

import pytest

from secret_store_client.client import Client, RPCError


TEST_CONFIG_PATH = '{}/configs/test_setup.conf'.format(
    os.path.dirname(os.path.realpath(__file__))
)


@pytest.fixture
def config():
    if not os.path.exists(TEST_CONFIG_PATH):
        pytest.fail('{} not found'.format(TEST_CONFIG_PATH))

    conf = {}
    with open(TEST_CONFIG_PATH) as config_file:
        for line in config_file.readlines():
            parts = line.split('=')
            if len(parts) != 2:
                continue

            key, value = parts
            conf[key] = value.strip('"').strip("'").strip('\n')

    return conf


def test_publish_and_consume_document(config):
    publisher = Client(
        config['ss_url'],
        config['parity_client_url'],
        config['publisher_address'],
        config['publisher_password']
    )

    document = 'mySecretDocument-{}'.format(uuid.uuid4())
    document_id = hashlib.sha256(document.encode()).hexdigest()
    encrypted = publisher.publish_document(document_id, document)

    consumer = Client(
        config['ss_url'],
        config['parity_client_url'],
        config['consumer_address'],
        config['consumer_password']
    )
    decrypted = consumer.decrypt_document(document_id, encrypted)

    assert document == decrypted


def test_rejects_keys_request_if_no_permissions(config):
    publisher = Client(
        config['ss_url'],
        config['parity_client_url'],
        config['publisher_address'],
        config['publisher_password']
    )

    # Noone has permissions to access this particular document
    # according to our test contract.
    document = 'mySecretDocument'
    document_id = hashlib.sha256(document.encode()).hexdigest()

    try:
        # Publish it if it was not already.
        publisher.publish_document(document_id, document)
    except Exception:
        pass

    consumer = Client(
        config['ss_url'],
        config['parity_client_url'],
        config['consumer_address'],
        config['consumer_password']
    )

    with pytest.raises(RPCError) as e:
        consumer.decrypt_document(document_id, '')

    assert 'Failed to retrieve decryption keys: Forbidden' == str(e.value)
