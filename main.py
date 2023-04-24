import requests
import json
from configparser import ConfigParser

class UrlConf(ConfigParser):
    def __init__(self, filename):
        super().__init__()
        self.read(filename, encoding="utf-8")
        
        
def checkValid(urls):
    valid_urls = []
    for url in urls:
        url = url.strip()
        share_id = url.split('/')[-1]
        data = json.dumps({'share_id':share_id})
        res = requests.post('https://api.aliyundrive.com/adrive/v3/share_link/get_share_by_anonymous?share_id='+share_id, data=data)
        res_data = json.loads(res.text)
        if 'code' in res_data.keys():
            if res_data['code']=='ShareLink.Cancelled':
                print(url+' 已失效')
        elif 'file_count' in res_data.keys():
            if res_data['file_count']==0:
                print(url+' 该分享无文件')
            else:
                print(url)
                valid_urls.append(url)
        else:
            print('出错啦')
    with open('./valid_url.txt', 'w') as f:
        f.write('\n'.join(valid_urls))
        f.close()
        
if __name__ =='__main__':
    conf = UrlConf('./conf.ini')
    urls = conf.get('urls', 'urls').split(',')

    checkValid(urls)