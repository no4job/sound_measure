__author__ = 'mishninDY'
import requests
from furl import *
import sys
# from bs4 import BeautifulSoup

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
client_id="QG8LA1VUNJLROPLT7ERTKPPE5CDVAT8GBIC8O60CG7SHFVRL4P7BTT6S4QLJAQ5K"
api_key = "924df66908664524b2ed1e6c2eda6867"
uuid = "59460be1a8ef482e8dbc531490b37688"
topic="queries"
user_agent = "Mozilla/5.0"
IN_DIR="../sound_level/yandex-cloud-sound-samples/queries/"

#Step 1
# ref_url = "http://asr.ru/oauth/authorize?response_type=code&client_id={client_id}&state={state}&redirect_uri={redirect_uri}"
# ref_url = "http://asr.yandex.net/asr_xml?uuid={uuid}&key={key}&topic={topic}"
ref_url = "https://asr.yandex.net/asr_xml?uuid={uuid}&key={key}&topic={topic}"
url=furl(ref_url).set(args={'uuid':uuid,'key':api_key,'topic':topic})
print(url)

headers={"Host":"asr.yandex.net", "Content-Type": "audio/x-wav"}

data = open(IN_DIR+"1.wav", 'rb').read()

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
# r = requests.post(url,  data=data, verify=verify , proxies=proxies, headers=headers)
r = requests.post( url=url,  data=data, headers=headers, proxies=proxies, verify=verify)
# r = requests.post( url=url,  files = {"1.wav":data}, headers=headers)
print(r.content)
for responce in r.history:
    print(responce.status_code,responce.reason)
#
# soup = BeautifulSoup(r.content)
# with open("resp.html", 'w+') as resp_f:
#     resp_f.write(soup.prettify())
# #print(soup.prettify())
# if "Вход на сайт" in soup.find_all("title")[0].text :
#     print ( soup.find_all("title")[0].text)
# elif "Предоставление доступа" in soup.find_all("title")[0].text :
#     print ( soup.find_all("title")[0].text)


sys.exit(0)
verify=False
#verify=True
#base_url="https://api.hh.ru/"
#command_url= "me"
scheme="https"
host="m.hh.ru"


command_url="oauth/authorize"
resource="oauth/authorize"

#access_token="I2FBHVENI01U2O2FNLORJPT5G4SF555BRVLB0V4KQMNLQN3TEP7H5P55479PG0BH"
headers={'User-Agent':'hhdata)', 'Host':'api.hh.ru','Accept':'*/*','Authorization':'Bearer '+ access_token}

r = requests.get(base_url+command_url, headers=headers, verify=verify )
print(r.content)

