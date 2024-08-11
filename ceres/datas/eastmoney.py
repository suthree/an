import json
import time

import execjs
import requests
from utils.base import get_data_by_keymap, trans_date_datetime


class EastMoney:
    """
    东方财富获取股票信息
    """

    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67",
        "Accept": "*/*",
        "DNT": "1",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Referer": "https://data.eastmoney.com/",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    }
    type_m_map = {
        "0": "深市",
        "1": "沪市",
        "3": "转债",
        "90": "板块",
        "116": "港股",
        "105": "美股",
    }
    stock_type_t_map = {
        "6": "深市主板",
        "80": "深市创业板",
        "8": "深市转债",
        "2": "沪市主板",
        "23": "沪市科创板",
        "4": "沪市转债",
    }
    topic_type_t_map = {
        "1": "地域概念",
        "2": "行业概念",
        "3": "概念板块",
    }
    code_type_mt = {
        "m:0+t:6",
        "m:0+t:80",
        # "m:0+t:81",
        # "m:0+t:8",
        "m:1+t:2",
        "m:1+t:23",
        # "m:1+t:4",
        "m:90+t:1",
        "m:90+t:2",
        "m:90+t:3",
        # "m:116 t:1",
        # "m:116 t:2",
        # "m:116 t:3",
        # "m:116 t:4",
        # "b:MK0354",  # 可转债
        # "s:2048",
    }
    code_type_fields = ",".join(code_type_mt)
    code_info_map = {
        "f12": "code",
        "f13": "type_m",
        "f14": "name",
        "f19": "type_t",
        "f20": "market_value",
        "f21": "float_value",
        "f9": "pe",
        "f23": "pb",
        "f26": "date",
    }
    code_info_fields = ",".join(code_info_map.keys())
    code_info_url = "http://push2.eastmoney.com/api/qt/clist/get"

    price_map = {
        "f2": "close",
        "f3": "change_rate",
        "f4": "change",
        "f5": "volume",
        "f6": "turnover",
        "f7": "amplitude",
        "f8": "turnover_rate",
        "f10": "volume_rate",
        "f12": "code",
        "f15": "high",
        "f16": "low",
        "f17": "open",
        "f18": "close_1",
        "f71": "average",
        "f109": "change_rate_5",
        "f124": "timestamp",
    }
    price_fields = ",".join(price_map.keys())
    money_map = {
        "f12": "code",
        # "f14": "name",
        "f62": "money_ma",
        "f184": "money_rate_ma",
        "f66": "money_sb",
        "f69": "money_rate_sb",
        "f72": "money_b",
        "f75": "money_rate_b",
        "f78": "money_m",
        "f81": "money_rate_m",
        "f84": "money_s",
        "f87": "money_rate_s",
        "f124": "timestamp",
    }
    money_fields = ",".join(money_map.keys())
    market_map = {}
    market_map.update(price_map)
    market_map.update(money_map)
    market_fields = ",".join(market_map.keys())

    price_history_fields = [
        "date",
        "open",
        "close",
        "high",
        "low",
        "volume",
        "turnover",
        "amplitude",
        "change_rate",
        "change",
        "turnover_rate",
    ]
    money_history_fields = [
        "date",
        "money_ma",
        "money_s",
        "money_m",
        "money_b",
        "money_sb",
        "money_rate_ma",
        "money_rate_s",
        "money_rate_m",
        "money_rate_b",
        "money_rate_sb",
        "close",
        "change_rate",
        "_",
        "_",
    ]
    sign_js = execjs.compile(open("ceres/datas/eastmoney_decrypt.js", "r").read())

    def get_params_cb(self):
        random_str = "1123048622946943576384"
        cb = f"jQuery{random_str}_{int(time.time() * 1000)}"
        return cb

    def get_response(self, url, params):
        cb = self.get_params_cb()
        params["cb"] = cb
        response = requests.get(url, headers=self.headers, params=params)
        return response

    def get_result(self, url, params):
        cb = self.get_params_cb()
        params["cb"] = cb
        response = self.get_response(url, params)
        try:
            tmp = response.text.replace(cb, "")
            return json.loads(tmp[1:-2]) or {}
        except:
            return {}

    def get_stock_info(self, page_num=1, page_size=10000):
        params = {
            "po": "1",
            "pn": page_num,
            "pz": page_size,
            "np": "1",
            "fltt": "2",
            "invt": "2",
            "fs": self.code_type_fields,
            "fields": self.code_info_fields,
        }
        result = self.get_result(self.code_info_url, params)
        datas = []
        for item in result.get("data", {}).get("diff", []):
            data = get_data_by_keymap(item, self.code_info_map, {"date": trans_date_datetime})
            if not data:
                continue
            datas.append(data)
        return datas

    def trans_stock_agu(self, code):
        if code.startswith("6"):
            return f"SH{code}"
        elif code.startswith("0") or code.startswith("3"):
            return f"SZ{code}"
        else:
            # TODO 转债 11 12
            return code

    def get_stock_topic(self, stock):
        url = "http://emweb.securities.eastmoney.com/CoreConception/PageAjax"
        params = {"code": self.trans_stock_agu(stock)}
        response = self.get_response(url, params)
        result = response.json()
        relations = result.get("ssbk", [])  # hxtc
        return relations

    def format_ts2date(self, ts, format="%Y-%m-%d"):
        return time.strftime(format, time.localtime(ts))

    def format_stock_market(self, data):
        data = get_data_by_keymap(data, self.market_map)
        timestamp = data.pop("timestamp")
        if not timestamp:
            return
        data["date"] = time.strftime("%Y-%m-%d", time.localtime(timestamp))
        return data

    def get_stock_market(self, page=1, page_size=10000):
        url = "http://push2.eastmoney.com/api/qt/clist/get"
        params = {
            "po": "1",
            "pn": page,
            "pz": page_size,
            "np": "1",
            "fltt": "2",
            "invt": "2",
            "fs": self.code_type_fields,
            "fields": self.market_fields,
        }
        result = self.get_result(url, params)
        datas = []
        for item in result.get("data", {}).get("diff", []):
            data = self.format_stock_market(item)
            if not data:
                continue
            datas.append(data)
        return datas

    def get_stock_market_history_price(self, code, klt="101", lmt="120", start_date="0", end_date="20500101"):
        url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            "beg": start_date,
            "end": end_date,
            "secid": code.strip(),  # '0.300059'
            "klt": klt,
            "lmt": lmt,
            "fqt": "1",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        }
        if klt != "101":
            params.update({"beg": "0", "smplmt": lmt, "lmt": "1000000"})
        result = self.get_result(url, params)
        datas = result.get("data", {}).get("klines", [])
        kdatas = [dict(zip(self.price_history_fields, i.split(","))) for i in datas]
        return kdatas

    def get_stock_market_history_money(self, code, klt="101", lmt="120", start_date="0", end_date="20500101"):
        url = "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"

        params = {
            "beg": start_date,
            "end": end_date,
            "secid": code,  # '0.300059'
            "lmt": lmt,
            "klt": klt,
            "fields1": "f1,f2,f3,f7",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
        }
        result = self.get_result(url, params)
        datas = result.get("data", {}).get("klines", [])
        kdatas = [dict(zip(self.money_history_fields, i.split(","))) for i in datas]
        return kdatas

    def get_stock_market_history(self, code, klt="101", lmt="120", start_date="0", end_date="20500101"):
        datas_price = self.get_stock_market_history_price(code, klt, lmt, start_date, end_date)
        datas_money = self.get_stock_market_history_money(code, klt, lmt, start_date, end_date)
        datas_date = {}
        for item in datas_price:
            date = item.get("date")
            if date:
                datas_date[date] = item
        for item in datas_money:
            date = item.get("date")
            if date:
                datas_date.setdefault(date, {}).update(item)
        return [datas_date[i] for i in sorted(datas_date.keys())]

    def get_todo(self):
        """
        TODO
        涨速
        人气
        股东人数
        牛散持股
        """
        pass



em = EastMoney()