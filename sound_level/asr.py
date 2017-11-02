__author__ = 'mishninDY'

import requests
import sys
import uuid
import os
import datetime
import time
import shutil
import json

#default request url
YANDEX_ASR_URL = "http://asr.yandex.net/asr_xml"
# YANDEX_ASR_URL = "http://10.85.132.50:3457/asr_xml"
#default  parameters
#github key
# API_KEY = "6372dda5-9674-4413-85ff-e9d0eb2f99a7"
#my key
API_KEY = "924df669-0866-4524-b2ed-1e6c2eda6867"
# API_KEY = "internal"
UUID_KEY = str(uuid.uuid4()).replace("-","")
TOPIC="queries"
#TOPIC="freeform"
#default  headers
# USER_AGENT = "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201"
HOST = "asr.yandex.net"
CONTENT_TYPE = "audio/x-wav"

#other default parameters
# IN_DIR="../sound_level/yandex-cloud-sound-samples/queries/"
IN_DIR = "../out/extracted_wav_fragments/"
# OUT_DIR="../sound_level/yandex-cloud-sound-samples/queries/"
OUT_DIR = "../out/extracted_wav_fragments/"
VERIFY=False
CHUNK_SIZE = 100000
MAX_INPUT_SIZE = 500000
RECOGNITION_RESULT_ROOT_PATH = "../recognition/"

#debug settings
USE_DEBUG_PROXY = False
if USE_DEBUG_PROXY:
    # proxies = {'http' : 'http://192.168.1.2:8888',
    #            'https': 'http://192.168.1.2:8888'}
    PROXIES = {'http' : 'http://127.0.0.1:8888',
               'https': 'http://127.0.0.1:8888'}

else:
    PROXIES = {}



def asrRequest(data,resultFileName,
               url=YANDEX_ASR_URL,uuid_key = UUID_KEY,api_key = API_KEY,topic = TOPIC,
               host = HOST,content_type = CONTENT_TYPE,
               proxies = PROXIES):

    params={'uuid':uuid_key,'key':api_key,'topic':topic}
    headers={"Host":host, "Content-Type": content_type}
    r = requests.post( url=url, params=params, data=data, headers=headers, proxies=proxies, verify=VERIFY)
    # if chunked:
    #     r = requests.post( url=url, params=params, data=data, headers=headers, proxies=proxies, verify=VERIFY)
    # else:
    #     r = requests.post( url=url, params=params, data=data, headers=headers, proxies=proxies, verify=VERIFY)
    print(r.status_code)
    print(r.content)
    with open(resultFileName, 'wb') as f:
        f.write(r.content)
        f.flush()

    return {"params":params,"status_code":r.status_code,"X-YaRequestId":r.headers["X-YaRequestId"]}

def gen(file,chunk_size = CHUNK_SIZE):
    count = 1
    with  open(file, 'rb') as f:
        while True:
            piece = f.read(chunk_size)
            if not piece:
                break
            print (count)
            count +=1
            yield piece
if __name__== "__main__":
    # fileForRecognition = "1.wav"
    # fileForRecognition = "test_15s_probki_glazki_hachalnik_yandex.wav"
    # fileForRecognition ="numbers_1_20.wav"
    # fileForRecognition ="all_text_16_part_1.wav"
    # comment = "generated voice, 0m 0s - 1m 08s text from cam9-1498221746-931 0h 9m 47.000s(587s) - 0h 12m 44.400s(764.4s) ~ 0h 2m 57.400s(177.400s)_subst.wav "
    fileForRecognition ="выводы_my_voice_12s_norm_-14dB.wav"
    comment = "my voice,  norm to -14dB , 12s from cam9-1498221746-931 0h 9m 47.000s(587s) - 0h 12m 44.400s(764.4s) ~ 0h 2m 57.400s(177.400s)_subst.wav "
    pathToFileForRecognition = IN_DIR+fileForRecognition
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S').replace(":","_")
    recognitionResultPath = RECOGNITION_RESULT_ROOT_PATH+os.path.splitext(fileForRecognition)[0]+"_"+st
    os.mkdir(recognitionResultPath)
    # recognizedFile = OUT_DIR+os.path.splitext(fileForRecognition)[0]+"_recognized"+".xml"
    recognizedFile = recognitionResultPath+"/"+os.path.splitext(fileForRecognition)[0]+"_recognized"+".xml"
    size = os.path.getsize(pathToFileForRecognition)
    src = pathToFileForRecognition
    dst = recognitionResultPath+"/"+fileForRecognition
    shutil.copyfile(src,dst)
    if size <= MAX_INPUT_SIZE:
        with open(pathToFileForRecognition, 'rb') as f:
            data = f.read()
            # recognizedFile = OUT_DIR+os.path.splitext(fileForRecognition)[0]+"_queries_recognized"+".xml"
            # asrRequest(data,recognizedFile)
            # recognizedFile = OUT_DIR+os.path.splitext(fileForRecognition)[0]+".xml"
            result = asrRequest(data,recognizedFile,topic="freeform")
    else:
        result = asrRequest(gen(pathToFileForRecognition),recognizedFile,topic="freeform")

    result["coment"] = comment
    with open(recognitionResultPath+"/"+'parameters.json', 'w') as fp:
        json.dump(result, fp)

sys.exit(0)



















