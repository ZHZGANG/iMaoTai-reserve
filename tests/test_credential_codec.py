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

class TestRealCredentials(TestCase):
    def setUp(self):
        self.credential_path = "./myConfig/credentials"
        self.base64_credential_path = self.credential_path + ".base64"
    def test_encode_decode_credentials(self):
        """test if config after encoding and then decoding is the same
        """
        expected_credential_count = 6
        config = ConfigParser()
        with open(self.base64_credential_path, "r") as f:
            decode(f.read(), config)
        self.assertEqual(len(config.sections()), expected_credential_count, "每当添加一个手机号，expected_credential_count需要相应增加 1，以此确保新加的手机号没有因为误操作被遗漏")

@skip("This test is like a tool to generate base64-encoded credential file of text credential, which you can run manually by comment this line out")
class TestBase64ForRealFile(TestCase):
    def setUp(self):
        self.credential_path = "./myConfig/credentials"
        self.base64_credential_path = self.credential_path + ".base64"
    def test_encode_to_file(self):
        configs_from_origin = ConfigParser()
        configs_from_origin.read(self.credential_path, encoding='utf-8')
        with open(self.base64_credential_path, "wb") as f:
            encode(configs_from_origin, f)
        with open(self.base64_credential_path, "r") as f:
            s = io.StringIO(f.read())
            configs_from_b64 = ConfigParser()
            decode(s.getvalue(), configs_from_b64)
            s.truncate(0)
            configs_from_b64.write(s)
        self.assertSetEqual(set(configs_from_b64.sections()), set(configs_from_origin.sections()))




if __name__ == '__main__':
    TestCase.main()
