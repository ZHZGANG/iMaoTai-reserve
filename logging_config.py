import logging
import datetime
import sys
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
TODAY = datetime.date.today().strftime("%Y%m%d")
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
                    stream=sys.stdout,
                    datefmt=DATE_FORMAT)