import io
import base64
from typing import BinaryIO, TypeVar
from unittest import TestCase,skip
from configparser import ConfigParser
from credential_codec import encode, decode
class TestEncodeDecode(TestCase):
    def setUp(self):
        self.config = ConfigParser()
        self.config_str = "[section]\nkey = value"
        self.config.read_string(self.config_str)

    def test_encode(self):
        """test if config after encoding and then decoding is the same
        """
        buffer = io.BytesIO()
        encode(self.config, buffer)
        new_config = ConfigParser()
        decode(buffer.getvalue().decode(), new_config)
        self.assertEqual(self.config, new_config)
        self.assertEqual(new_config.get("section", "key"), "value")

    @skip("This test is like a tool to generate base64-encoded credential file of text credential")
    def test_encode_to_file(self):
        credential_path = "./myConfig/credentials"
        cf = ConfigParser()
        cf.read(credential_path, encoding='utf-8')
        with open(credential_path+".base64", "wb") as f:
            encode(cf, f)

if __name__ == '__main__':
    TestCase.main()
