import configparser
import os
import config as cf
import process
import privateCrypt
import base64
import credential_codec
import logging_config
import logging
import click

config = configparser.ConfigParser()  # 类实例化

def get_credentials_path():
    if cf.CREDENTIALS_PATH is not None:
        return cf.CREDENTIALS_PATH
    else:
        home_path = os.getcwd()
        config_parent_path = os.path.join(home_path, 'myConfig')
        config_path = os.path.join(config_parent_path, 'credentials')
        if not os.path.exists(config_parent_path):
            os.mkdir(config_parent_path)
        return config_path

if cf.CREDENTIALS_BASE64:
    # 将 base64编码的字符串解码后，导入 config
    logging.info("Get credentials from env 'CREDENTIALS_BASE64'")
    credential_codec.decode(cf.CREDENTIALS_BASE64, config)
else:
    logging.info("Get credentials from file")
    path = get_credentials_path()
    # 这里config需要用encoding，以防跨平台乱码
    config.read(path, encoding="utf-8")
sections = config.sections()
logging.info(f"Config sections: {sections}")


def get_location():
    while 1:
        location = input(f"请输入精确小区位置，例如[小区名称]，为你自动预约附近的门店:").strip()
        selects = process.select_geo(location)

        a = 0
        for item in selects:
            formatted_address = item['formatted_address']
            province = item['province']
            print(f'{a} : [地区:{province},位置:{formatted_address}]')
            a += 1
        user_select = input(f"请选择位置序号,重新输入请输入[-]:").strip()
        if user_select == '-':
            continue
        select = selects[int(user_select)]
        formatted_address = select['formatted_address']
        province = select['province']
        print(f'已选择 地区:{province},[{formatted_address}]附近的门店')
        return select

@click.command()
@click.option('--simple-mode', '-s', is_flag=True, help='是否使用简单模式，号码存在时跳过', required=False)
def login(simple_mode):
    aes_key = privateCrypt.get_aes_key()

    while 1:
        process.init_headers()

        # 获取手机号
        mobile = input("输入手机号[13812341234]:").strip()
        encrypt_mobile = privateCrypt.encrypt_aes_ecb(mobile, aes_key)


        # 只有当非简易模式，或号码不存在时，
        # 才需要需要设置位置，否则沿用之前的位置信息
        relocate: bool = False
        if (not simple_mode) or (not config.has_section(encrypt_mobile)):
            relocate = True

        if not config.has_section(encrypt_mobile):
            config.add_section(encrypt_mobile)  # 首先添加一个新的section

        if relocate:
            # 获取位置信息
            logging.info("skip location setting in simple mode.")
            location_select: dict = get_location()
            province = location_select['province']
            city = location_select['city']
            location: str = location_select['location']
            config.set(encrypt_mobile, 'province', str(province))
            config.set(encrypt_mobile, 'city', str(city))
            config.set(encrypt_mobile, 'lat', location.split(',')[1])
            config.set(encrypt_mobile, 'lng', location.split(',')[0])

        process.get_vcode(mobile)
        code = input(f"输入 [{mobile}] 验证码[1234]:").strip()
        token, userId = process.login(mobile, code)

        endDate = input(f"输入 [{mobile}] 截止日期(必须是YYYYMMDD,20230819)，如果不设置截止，请输入9：").strip()

        # 为了增加辨识度，这里做了隐私处理，不参与任何业务逻辑
        hide_mobile = mobile.replace(mobile[3:7], '****')
        # 因为加密了手机号和Userid，所以token就不做加密了
        encrypt_userid = privateCrypt.encrypt_aes_ecb(str(userId), aes_key)

        config.set(encrypt_mobile, 'hidemobile', hide_mobile)
        config.set(encrypt_mobile, 'enddate', endDate)
        config.set(encrypt_mobile, 'userid', encrypt_userid)
        config.set(encrypt_mobile, 'token', str(token))


        path = get_credentials_path()
        # 保存数据
        with open(path, 'w', encoding="utf-8") as f:
            config.write(f)

        # 将配置文件转为 base64编码，可以作为 secrets 放在 github secrets 中
        with open(path+".base64", "wb") as base64_file:
            credential_codec.encode(config, base64_file)

        condition = input(f"是否继续添加账号[y/n]:").strip()

        if condition.lower() == 'n':
            break

if __name__ == '__main__':
    login()