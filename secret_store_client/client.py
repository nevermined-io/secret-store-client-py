import json
import requests


JSON_CONTENT = {'Content-Type': 'application/json'}


class RPCError(Exception):
    pass


class Client:
    """Connects to Secret Store and Parity Ethereum client.
       Publishes and consumes documents.
    """

    def __init__(self, secret_store_url, parity_client_url, address, password):
        self.secret_store_url = secret_store_url
        self.parity_client_url = parity_client_url
        self.address = address
        self.password = password

    def publish_document(self, document_id, document, threshold=0):
        """ Encrypts and publishes the given unencrypted document identified
            by the given ID.

            See https://wiki.parity.io/Secret-Store-Tutorial-2.html.

            Returns the encrypted document.
        """
        signed = self._sign_document(document_id)
        server_key = self._generate_server_key(document_id, signed,
                                               threshold=threshold)
        key_data = self._generate_document_key(server_key)
        encrypted = self._encrypt(key_data['encrypted_key'],
                                  document.encode().hex())

        self._store_document_key(document_id, signed,
                                 key_data['encrypted_point'],
                                 key_data['common_point'])
        return encrypted

    def decrypt_document(self, document_id, encrypted_document):
        """ Decrypts the given encrypted document identified by the given ID.

            See https://wiki.parity.io/Secret-Store-Tutorial-3.html.

            Returns the decrypted document.
        """
        signed = self._sign_document(document_id)

        key_data = self._get_decryption_keys(document_id, signed)
        decrypted_hex = self._decrypt(key_data['decrypted_secret'],
                                      key_data['common_point'],
                                      key_data['decrypt_shadows'],
                                      encrypted_document)

        return bytearray.fromhex(decrypted_hex[2:]).decode()

    def _sign_document(self, document_id):
        payload = json.dumps({
            'jsonrpc': '2.0',
            'method': 'secretstore_signRawHash',
            'params': [self.address, self.password,
                       '0x' + document_id],
            'id': 1
        })
        resp = requests.post(self.parity_client_url, data=payload,
                             headers=JSON_CONTENT)

        self._handle_error(resp, 'Failed to sign the document')

        return resp.json()['result']

    def _generate_server_key(self, document_id, signed_document_key,
                             threshold):
        url = '{}/shadow/{}/{}/{}'.format(self.secret_store_url, document_id,
                                          signed_document_key[2:],
                                          threshold)
        resp = requests.post(url)

        self._handle_error(resp, 'Failed to generate server key')

        return resp.json()

    def _generate_document_key(self, server_key):
        payload = json.dumps({
            'jsonrpc': '2.0',
            'method': 'secretstore_generateDocumentKey',
            'params': [self.address, self.password, server_key],
            'id': 1
        })
        resp = requests.post(self.parity_client_url, data=payload,
                             headers=JSON_CONTENT)

        self._handle_error(resp, 'Failed to generate the document key')

        return resp.json()['result']

    def _encrypt(self, encrypted_key, document_hex):
        payload = json.dumps({
            'jsonrpc': '2.0',
            'method': 'secretstore_encrypt',
            'params': [self.address, self.password, encrypted_key,
                       '0x' + document_hex],
            'id': 1
        })
        resp = requests.post(self.parity_client_url, data=payload,
                             headers=JSON_CONTENT)

        self._handle_error(resp, 'Failed to encrypt the document')

        return resp.json()['result']

    def _store_document_key(self, document_id, signed_document_id,
                            encrypted_point, common_point):
        url = '{}/shadow/{}/{}/{}/{}'.format(self.secret_store_url,
                                             document_id,
                                             signed_document_id[2:],
                                             common_point[2:],
                                             encrypted_point[2:])
        resp = requests.post(url)

        self._handle_error(resp, 'Failed to store the document key')

    def _get_decryption_keys(self, document_id, signed_document_id):
        url = '{}/shadow/{}/{}'.format(self.secret_store_url,
                                       document_id,
                                       signed_document_id[2:])
        resp = requests.get(url)

        self._handle_error(resp, 'Failed to retrieve decryption keys')

        return resp.json()

    def _decrypt(self, decrypted_secret, common_point,
                 decrypted_shadows, encrypted_document):
        payload = json.dumps({
            'jsonrpc': '2.0',
            'method': 'secretstore_shadowDecrypt',
            'params': [self.address, self.password, decrypted_secret,
                       common_point, decrypted_shadows,
                       encrypted_document],
            'id': 1
        })
        resp = requests.post(self.parity_client_url, data=payload,
                             headers=JSON_CONTENT)

        self._handle_error(resp, 'Failed to encrypt the document')

        return resp.json()['result']

    def _handle_error(self, resp, message):
        try:
            data = resp.json()
        except Exception:
            pass
        else:
            if 'error' in data:
                error = data['error'] if isinstance(data, dict) else data
                raise RPCError('{}: {}'.format(message, error))

        if resp.status_code != 200:
            raise RPCError('{}: {}'.format(message, resp.reason))
