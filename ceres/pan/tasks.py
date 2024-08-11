import ipdb
from datas.eastmoney import em
from pan.models import StockInfo
from pypinyin import Style, lazy_pinyin, pinyin


def get_all_first_letters(chinese_str):
    """
    输出首字母缩写，方便检索
    """
    first_letters = [char[0].upper() for char in lazy_pinyin(chinese_str)]
    return "".join(first_letters)
    # 多音字
    first_letters = []
    for char_pinyin in pinyin(chinese_str, style=Style.FIRST_LETTER):
        first_letters.extend([pinyin[0] for pinyin in char_pinyin])
    return first_letters


def update_stock_info():
    # source = DataSourceChoice.DATA_SOURCE_EM
    infos = []
    datas = em.get_stock_info()
    ipdb.set_trace()
    for data in datas[:3]:
        code = data["code"]
        name = data["name"]
        name_pinyin = get_all_first_letters(name)
        # TODO name 改变则names 增量更新搜索条件
        data["names"] = ",".join([code, name, name_pinyin])
        info_obj = StockInfo(**data)
        # StockInfo.objects.update_or_create(code=code, defaults=datas)
        infos.append(info_obj)
    StockInfo.objects.bulk_create(infos)


def update_stock_market_day(code, date, data):
    """更新股票日线数据"""
    pass
