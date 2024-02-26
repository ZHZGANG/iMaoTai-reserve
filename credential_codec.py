"""credentials encoding and decoding"""
import base64
from typing import BinaryIO, TextIO
from typing import TypeVar, Type
from configparser import ConfigParser
import io

ConfigParserType = TypeVar("ConfigParserType", bound="ConfigParser")
def encode(config: ConfigParserType, output: BinaryIO):
    """convert bytes of .ini into base64 bytes, which can be stored as Github Secret

    Args:
        config (ConfigParserType): _description_
        output (BinaryIO): _description_
    """
    # 将配置文件转为 base64编码，可以作为 secrets 放在 github secrets 中
    buffer = io.StringIO()
    config.write(buffer)
    buffer_bytes = buffer.getvalue().encode('utf-8')
    encoded_config_data = base64.b64encode(buffer_bytes)
    output.write(encoded_config_data)

def decode(buff: str, config: ConfigParserType):
    """ b64decode str from environ, and save it to config

    Args:
        buff (str): _description_
        config (ConfigParserType): _description_
    """
    raw_config = base64.b64decode(buff)
    config.read_string(raw_config.decode('utf-8'))