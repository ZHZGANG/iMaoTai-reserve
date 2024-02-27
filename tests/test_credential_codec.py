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
    def test_chinese_codec(self):
        """test if config after encoding and then decoding is the same
        """
        original_config = ConfigParser()
        original_config.read_string("[组]\n键 = 值")
        buffer = io.BytesIO()
        encode(original_config, buffer)
        new_config = ConfigParser()
        decode(buffer.getvalue().decode(), new_config)
        self.assertEqual(original_config, new_config)
        self.assertEqual(new_config.get("组", "键"), "值")


@skip("This test is like a tool to generate base64-encoded credential file of text credential")
class TestBase64ForRealFile(TestCase):
    def setUp(self):
        self.credential_path = "./myConfig/credentials"
        self.base64_credential_path = self.credential_path + ".base64"
    def test_encode_to_file(self):
        cf = ConfigParser()
        cf.read(self.credential_path, encoding='utf-8')
        with open(self.base64_credential_path, "wb") as f:
            encode(cf, f)
        with open(self.base64_credential_path, "r") as f:
            s = io.StringIO(f.read())
            cp = ConfigParser()
            decode(s.getvalue(), cp)
            s.truncate(0)
            cp.write(s)
            print(s.getvalue())




if __name__ == '__main__':
    TestCase.main()
