import requests
import time


def get_balance(token):
    balance_url = 'https://api.quackquack.games/balance/get'
    headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,zh-CN;q=0.7,zh;q=0.6',
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://dd42189ft3pck.cloudfront.net',
    'Referer': 'https://dd42189ft3pck.cloudfront.net/',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}
    response = requests.get(balance_url, headers=headers)
    if response.status_code == 200:
        balances = response.json().get('data', {}).get('data', [])
        egg_balance_info = next((item for item in balances if item['symbol'] == 'EGG'), None)
        if egg_balance_info:
            return egg_balance_info['balance']
        else:
            return "Không tìm thấy thông tin balance của EGG."
    else:
        return "Lỗi khi lấy balance."
def get_nest_ids(token):
    list_url = 'https://api.quackquack.games/nest/list-reload'
    headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,zh-CN;q=0.7,zh;q=0.6',
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://dd42189ft3pck.cloudfront.net',
    'Referer': 'https://dd42189ft3pck.cloudfront.net/',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

    response = requests.get(list_url, headers=headers)
    if response.status_code == 200:
        nest_data = response.json().get('data', {}).get('nest', [])
        return [(nest['id'], nest.get('type_egg')) for nest in nest_data]
    else:
        print("Không thể lấy danh sách nest. Mã lỗi:", response.status_code)
        return []

def collect_nest(nest_id, token):
    collect_url = 'https://api.quackquack.games/nest/collect'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,zh-CN;q=0.7,zh;q=0.6',
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://dd42189ft3pck.cloudfront.net',
        'Referer': 'https://dd42189ft3pck.cloudfront.net/',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    data = {'nest_id': nest_id}
    response = requests.post(collect_url, headers=headers, data=data)
    return response

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjExMDAwMjcsInRpbWVzdGFtcCI6MTcyMTA0NDI4NDc2NCwidHlwZSI6MSwiaWF0IjoxNzIxMDQ0Mjg0LCJleHAiOjE3MjE2NDkwODR9.hhgWdflou7jS_KjJGUCg24uZfWo31jFn0UnjR1GNTZk'

while True:
    nest_ids = get_nest_ids(token)

    for nest_id, type_egg in nest_ids:
        if type_egg is None:
            continue
        response = collect_nest(nest_id, token)
        response_data = response.json()  
        balance = get_balance(token)

        if response.status_code == 200 and response_data.get("error_code") == "":
            result_message = "Thành công"
        elif response_data.get("error_code") == "THIS_NEST_DONT_HAVE_EGG_AVAILABLE":
            result_message = "Thất bại - Tổ này không có trứng"
        else:
            result_message = "Lỗi không xác định"

        print(f"Thu hoạch ổ trứng {nest_id}: Status {response.status_code}, Kết quả: {result_message}, EGG balance: {balance}")

        time.sleep(5)
#nghỉ 10s mỗi lượt
time.sleep(10)