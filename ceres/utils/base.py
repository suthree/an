import time
from datetime import datetime

date_f_0 = "%Y%m%d"
date_f_1 = "%Y-%m-%d"
date_f_2 = "%Y-%m-%d %H:%M"
date_f_3 = "%Y-%m-%d %H:%M:%S"


def trans_timestamp_datetime(ts, date_f=date_f_1):
    return time.strftime(date_f, time.localtime(ts))


def trans_date_datetime(date_str: str | int, date_f=date_f_0, date_t=date_f_1):
    return datetime.strptime(str(date_str), date_f).strftime(date_t)


def trans_datetime_timestamp(date_str):
    for date_f in [date_f_3, date_f_2, date_f_1, date_f_0]:
        try:
            return int(datetime.strptime(date_str, date_f).timestamp())
        except:
            pass


def check_need_fields(data, keys=["open", "close", "high", "low"]):
    # 退市的票 没有收盘价格
    # 停牌的票 没有开盘
    for k in keys:
        v = data.get(k)
        if not v:
            return
        if not (isinstance(v, str) or isinstance(v, float)):
            return
    return True


def get_data_by_keymap(data, key_map={}, func_map={}):
    if not key_map:
        return data
    datas = {}
    for raw_key, want_key in key_map.items():
        data_v = data.get(raw_key)
        if data_v == "-":  # 兼容东财的 -
            data_v = None
        if data_v:
            if func_map:
                data_v = func_map.get(raw_key, lambda x: x)(data_v)
        datas[want_key] = data_v
    return datas
