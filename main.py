import datetime
import logging_config
import logging
import sys

import config
import login
import process
import privateCrypt
import report
from statistics import Statistics, UserResult

from notify import PushplusNotifier

TODAY = datetime.date.today().strftime("%Y%m%d")

process.get_current_session_id()

# 校验配置文件是否存在
configs = login.config
if len(configs.sections()) == 0:
    logging.error("配置文件未找到配置")
    sys.exit(1)

aes_key = privateCrypt.get_aes_key()

s_title = '茅台预约成功'
s_content = ""

stat = Statistics()
for user_section in configs.sections():
    if (configs.get(user_section, 'enddate') != 9) and (TODAY > configs.get(user_section, 'enddate')):
        continue
    mobile = privateCrypt.decrypt_aes_ecb(user_section, aes_key)
    province = configs.get(user_section, 'province')
    city = configs.get(user_section, 'city')
    token = configs.get(user_section, 'token')
    userId = privateCrypt.decrypt_aes_ecb(configs.get(user_section, 'userid'), aes_key)
    lat = configs.get(user_section, 'lat')
    lng = configs.get(user_section, 'lng')

    p_c_map, source_data = process.get_map(lat=lat, lng=lng)

    process.UserId = userId
    process.TOKEN = token
    process.init_headers(user_id=userId, token=token, lng=lng, lat=lat)
    user_result = UserResult(mobile)
    # 根据配置中，要预约的商品ID，城市 进行自动预约
    try:
        for item in config.ITEM_CODES:
            max_shop_id = process.get_location_count(province=province,
                                                     city=city,
                                                     item_code=item,
                                                     p_c_map=p_c_map,
                                                     source_data=source_data,
                                                     lat=lat,
                                                     lng=lng)
            # print(f'max shop id : {max_shop_id}')
            if max_shop_id == '0':
                user_result.add_failure()
                continue
            shop_info = source_data.get(str(max_shop_id))
            title = config.ITEM_MAP.get(item)
            polished_reservation_info = f'商品:{title};门店:{shop_info["name"]}'
            logging.info(polished_reservation_info)
            reservation_params = process.act_params(max_shop_id, item)
            # 核心预约步骤
            r_success, reserve_result_text = process.reservation(reservation_params, mobile)
            if not r_success:
                user_result.add_failure(1, reserve_result_text+polished_reservation_info)
            else:
                user_result.add_success(1, reserve_result_text+polished_reservation_info)
        # 领取小茅运和耐力值
        process.getUserEnergyAward(mobile)
        stat.update(user_result)
    except BaseException as e:
        print(e)
        logging.error(e)

result = report.TextReport(stat, '茅台预约成功', '')
report_title, report_body = result.build()

# 推送消息
push = PushplusNotifier(token=config.PUSH_TOKEN)
push.send(report_title, report_body)
