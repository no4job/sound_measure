__author__ = 'mishninDY'
import requests
import sys
import codecs
import os

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
def splitFile(file,limit=2000):
    partLength = 0
    count = -1
    part = []
    for s in f.read().splitlines():
        if len(s.encode("utf8")) > limit:
            return None
        if count == -1:
            part.append(s)
            count = 0
            continue
        if len(part[count].encode("utf8")) + len(s.encode("utf8")) > limit:
            part.append(s)
            count+=1
        else:
            part[count]=part[count]+" "+s
    return part

if __name__== "__main__":
    tts_string = False
    tts_by_list = False
    tts_file = True
    FILE_DIR =  "../out/extracted_wav_fragments/"
    FILE_NAME = "all_text.txt"
    LIST_DIR = "../replacement/"
    LIST_NAME = "replacement_list.txt"
    # TEXT = "задержанной"
    # TEXT = "1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 15. 16. 17. 18. 19. 20."
    # TEXT = "Какие ... выводы-то для себя какие-то делаете вы. Естественно. Вам еще повезло что вы с таким стажем богатым первый раз только на скамье подсудимых оказались."
    TEXT = "тест"
    # OUT_DIR = LIST_DIR
    # OUT_DIR="../out/extracted_wav_fragments/"
    OUT_DIR = FILE_DIR
    # speechSoundFileName = "tts.wav"
    #speechSoundFileName = "numbers_1_20.wav"
    #speechSoundFileName = "выводы.wav"
    # speechSoundFileName = "тест.wav"
    speechSoundFileName = "all_text.wav"

    speed = 1


    # ttsList = OUT_DIR+"replacement_list.txt"
    # ttsTextFile = "all_text.txt"
    # ttsTextPath = "../out/extracted_wav_fragments/"+ttsTextFile

    ttsList = []
    if tts_by_list:
        listPath = LIST_DIR+LIST_NAME
        with codecs.open(listPath, 'r',"utf-8") as f:
            #tts limited with  limit of TTS API = 2000 symbols
            ttsList = f.read().splitlines()
    elif tts_string:
        ttsList = [TEXT]
    elif tts_file:
        filePath = FILE_DIR+FILE_NAME
        with codecs.open(filePath, 'r',"utf-8") as f:
            ttsList = splitFile(f)
    else:
        sys.exit(0)
    # for replacementText in f.read().splitlines() :

    count = 0
    for tts in ttsList :
        print(tts)
        if tts_by_list:
            speechSoundFilePath = OUT_DIR+tts+".wav"
            ttsRequest(tts,speechSoundFilePath,quality = "hi",speed = speed)
        elif tts_string:
            speechSoundFilePath = OUT_DIR+speechSoundFileName
            ttsRequest(tts,speechSoundFilePath,quality = "hi",speed = speed)
        elif tts_file:
            speechSoundFilePath = OUT_DIR+os.path.splitext(speechSoundFileName)[0]+"_part_{}".format(count+1)+".wav"
            ttsRequest(tts,speechSoundFilePath,quality = "hi",speed = speed)
        else:
            sys.exit(0)
        count+=1
sys.exit(0)



