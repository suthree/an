import requests

url = "https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/stock?stock_type=a&type=hour&list_type=normal"

payload = {}
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
    "Host": "dq.10jqka.com.cn",
    "Cache-Control": "no-cache",
    "Cookie": "v=A9-nfFuzxd4GI8HCXCGEO4CBbjZpRDPmTZg32nEsew7VAP0jeRTDNl1oxyuC; escapename=%25u683c%25u5b50%25u95f4%25u7684%25u591c%25u665a; user=MDq48dfTvOS1xNK5ze06Ok5vbmU6NTAwOjUyMDgzMjc1OTo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNTo6OjUxMDgzMjc1OToxNzIzODY5NzA0Ojo6MTU4MjE1MzUwMDoyNjc4NDAwOjA6MTQ4M2UwZmNhNjVjMDNkMDAxMzAxOTViMGViMjMwYmU2Ojox; ticket=b7c01ae5aa5947fbb7c8e24e23c83759; userid=510832759; u_name=%B8%F1%D7%D3%BC%E4%B5%C4%D2%B9%CD%ED; user_status=0",
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


import requests

url = "http://m.domekj.top/hjbd/gp.txt"

payload = {}
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)",
    "Host": "m.domekj.top",
    "Pragma": "no-cache",
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
