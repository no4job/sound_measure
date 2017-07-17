__author__ = 'mishninDY'
import requests
import sys
import codecs


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
verify=True
#verify=False


OUT_DIR="../replacement/"
YANDEX_TTS_URL = "https://tts.voicetech.yandex.net/generate"
#request parameters
#github api key
# API_KEY = "6372dda5-9674-4413-85ff-e9d0eb2f99a7"
#my api key
API_KEY = "924df669-0866-4524-b2ed-1e6c2eda6867"

def ttsRequest(text,fileName,url=YANDEX_TTS_URL,format = "wav",quality = "hi",lang = "ru-RU",speaker = "oksana",speed = 1.0,emotion = "good"):
    # format = "wav"
    # quality = "hi"
    # lang = "ru-RU"
    # speaker = "oksana"
    # speed = 1.0
    # # emotion = "neutral"
    # emotion = "good"
    params = {"key":API_KEY,"text" : text, "format": format,"quality":quality,"lang":lang,"speaker":speaker,
              "speed":speed,"emotion":emotion}
    r = requests.get( url=url, params=params, proxies=proxies, verify=verify)
    print(r.status_code)
    # print(r.content)
    # print(sys.getfilesystemencoding()+"\n")
    with open(fileName, 'wb') as f:
    # with open(IN_DIR+"", 'wb') as f:
            f.write(r.content)
            f.flush()
    # for responce in r.history:
    #     print(responce.status_code,responce.reason)

if __name__== "__main__":
    text = "задержанной"
    tts_by_list = False
    # with open(OUT_DIR+"replacement_list.txt", 'r') as f:
    with codecs.open(OUT_DIR+"replacement_list.txt", 'r',"utf-8") as f:
        # replacementList = f.readlines()
        if tts_by_list:
            ttsList = f.read().splitlines()
        else:
            ttsList = [text]
        # for replacementText in f.read().splitlines() :
        for tts in ttsList :
            print(tts)
            # speechFileName = OUT_DIR+replacementText+"_low"+".wav"
            speechFileName = OUT_DIR+tts+".wav"
            ttsRequest(tts,speechFileName,quality = "hi")
sys.exit(0)



