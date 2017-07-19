__author__ = 'mishninDY'
import requests
from furl import *
import sys
import uuid

'''
Get information about proxy: request.py:getproxies_environment()
Windows proxy settings:
[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings]
"MigrateProxy"=dword:00000001
"ProxyEnable"=dword:00000001
"ProxyHttp1.1"=dword:00000000
"ProxyServer"="http://ProxyServername:80"
"ProxyOverride"="<local>

Ubuntu proxy settings
configuration file:cat /etc/environment  (cat /etc/environment)->
http_proxy="http://127.0.0.1:8888/"
https_proxy="https://127.0.0.1:8888/"

system environment variables (printenv | grep -i proxy)->
NO_PROXY=localhost,127.0.0.0/8,::1
http_proxy=http://127.0.0.1:8888/
https_proxy=https://127.0.0.1:8888/
no_proxy=localhost,127.0.0.0/8,::1

reload changed variables from /etc/environment need logout->login or reboot

copy proxy SSL certificate file(PEM) to  /etc/ssl/certs/ca-certificates.crt/
sudo update-ca-certificates
'''
#github key
# api_key = "6372dda5-9674-4413-85ff-e9d0eb2f99a7"
#for_asr key
api_key = "4f49da7e-7070-4fe6-beaf-52bdf1650e98"
#my key
# api_key = "924df669-0866-4524-b2ed-1e6c2eda6867"
uuid = str(uuid.uuid4()).replace("-","")
topic="queries"
user_agent = "Mozilla/5.0"
IN_DIR="../sound_level/yandex-cloud-sound-samples/queries/"

# ref_url = "http://asr.yandex.net/asr_xml?uuid={uuid}&key={key}&topic={topic}"
# url=furl(ref_url).set(args={'uuid':uuid,'key':API_KEY,'topic':topic})
# print(url)

url = "http://asr.yandex.net/asr_xml"
params={'uuid':uuid,'key':api_key,'topic':topic}

# headers={"Host":"asr.yandex.net", "Content-Type": "audio/x-wav","User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"}
headers={"Host":"asr.yandex.net", "Content-Type": "audio/x-wav","User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"}
with open(IN_DIR+"1.wav", 'rb') as f:
    data = f.read()

#debug proxy - manual setting, for external debug   proxy
use_debug_proxy = False
#use_debug_proxy = True
if use_debug_proxy:
    # proxies = {'http' : 'http://192.168.1.2:8888',
    #            'https': 'http://192.168.1.2:8888'}
    proxies = {'http' : 'http://127.0.0.1:8888',
               'https': 'http://127.0.0.1:8888'}

else:
    proxies = {}
#verify=True
verify=False

r = requests.post( url=url, params=params, data=data, headers=headers, proxies=proxies, verify=verify)
# r = requests.post( url=url,  files = {"1.wav":data}, headers=headers)
print(r.status_code)
print(r.content)
#
# for responce in r.history:
#     print(responce.status_code,responce.reason)


sys.exit(0)


