import urllib.parse
import subprocess
from functools import partial
import execjs

def get_a_b(params, headers):
    subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')  # 继续保持此行
    
    # params_str = urllib.parse.urlencode(params)
    # with open(r'C:/Users/13973/Desktop/Start/code/pycode/dycode/jscode/douyin.js', 'r', encoding='utf-8') as f:
    #     js_code = f.read()
    # a_bogus = execjs.compile(js_code).call('get_a_bogus', params_str)
    # params['a_bogus'] = a_bogus
    DOUYIN_SIGN = execjs.compile(open(r'pyc\\utils\\douyin1.js', encoding='utf-8').read())
    query = '&'.join([f'{k}={urllib.parse.quote(str(v))}' for k, v in params.items()])
    headers = headers
    headers['user-agent'] = ''
    a_bogus = DOUYIN_SIGN.call('sign_reply', query, headers)
    params["a_bogus"] = a_bogus
    return params