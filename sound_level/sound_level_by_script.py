__author__ = 'mishninDY'
__author__ = 'mishninDY'
import os
import subprocess
import json
import math
import csv
import pprint
# print (os.getcwd())
FFMPEG_DIR="..\\FFMPEG\\BIN\\"
IN_DIR="../IN/"
OUT_DIR="../OUT"
r128_FRAME_DURATION=0.1
SHORT_FRAME_DURATION = 5
LONG_FRAME_DURATION = SHORT_FRAME_DURATION*36 # 5*36=180s = 3 min
SHORT_FRAME_SIZE=SHORT_FRAME_DURATION // r128_FRAME_DURATION
LONG_FRAME_SIZE=LONG_FRAME_DURATION // r128_FRAME_DURATION
#inputFileName = "test.wav"
#inputFilePath="H\\\\:/Полезное видео/Распознавание речи/cs229 - video/CS229-lecture10.mp4"
inputFilePath="..\\IN\\test.wav"
# inputFilePath=IN_DIR+"/"+inputFileName
#ffprobeLavfiStr="amovie={},ebur128=metadata=1:peak=true".format(inputFilePath)
#ffprobeLavfiStr="amovie={},ebur128=metadata=1:peak=true".format(inputFilePath)
tmpFilePath=OUT_DIR+"/tmp.mkv"
ffprobeLavfiStr="amovie={},ebur128=metadata=1:peak=true".format(tmpFilePath)
ffmpegFilterStr="ebur128=metadata=1:peak=true"
# process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR), "-f", "lavfi","-i", "amovie=../in/test.wav,ebur128=metadata=1:peak=true","-show_frames", "-show_format", "-print_format", "json"], stdout=subprocess.PIPE,shell=True)
# process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR), "-f", "lavfi","-i", filterStr,"-show_frames", "-show_format", "-print_format", "json"], stdout=subprocess.PIPE,shell=True)
# *** process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR), "-f", "lavfi","-i", "amovie=H\\\\:/Полезное видео/Распознавание речи/cs229 - video/CS229-lecture10.mp4,ebur128=metadata=1:peak=true","-show_frames", "-show_format", "-print_format", "json"], stdout=subprocess.PIPE)
process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR), tmpFilePath,"-show_format", "-print_format", "json"], stdout=subprocess.PIPE)
stdout = process.communicate()[0]
parsed =  json.loads(stdout)
duration=float(parsed["format"]["duration"])
process = subprocess.Popen(["{}ffmpeg".format(FFMPEG_DIR),"-y","-i",inputFilePath, "-c","copy",tmpFilePath], stdout=subprocess.PIPE)
process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR), "-f", "lavfi","-i", ffprobeLavfiStr,"-show_frames", "-show_format", "-print_format", "json"], stdout=subprocess.PIPE)
# process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR), "-f", "lavfi","-i", filterStr,"-show_frames", "-show_format", "-print_format", "json"], stdout=subprocess.PIPE)
stdout = process.communicate()[0]
print ('STDOUT:{}'.format(stdout))
parsed =  json.loads(stdout)
lavfi_r128_M = []
lavfi_r128_S = []
lavfi_r128_I = []
lavfi_r128_LRA = []
lavfi_r128_LRA_low = []
lavfi_r128_LRA_high = []
lavfi_r128_true_peaks_ch0 = []
lavfi_r128_true_peaks_ch1 = []
lavfi_r128_used = []
for frame in parsed["frames"]:
    if "tags" in frame:
        tags=frame["tags"]
        lavfi_r128_used.append(1)
        lavfi_r128_M.append(float(tags["lavfi.r128.M"]))
        lavfi_r128_S.append(float(tags["lavfi.r128.S"]))
        lavfi_r128_I.append(float(tags["lavfi.r128.I"]))
        lavfi_r128_LRA.append(float(tags["lavfi.r128.LRA"]))
        lavfi_r128_LRA_low.append(float(tags["lavfi.r128.LRA.high"]))
        lavfi_r128_LRA_high.append(float(tags["lavfi.r128.LRA.low"]))
        lavfi_r128_true_peaks_ch0.append(float(tags["lavfi.r128.true_peaks_ch0"]))
        lavfi_r128_true_peaks_ch1.append(float(tags["lavfi.r128.true_peaks_ch1"]))
    else:
        lavfi_r128_used.append(0)
        lavfi_r128_M.append(None)
        lavfi_r128_S.append(None)
        lavfi_r128_I.append(None)
        lavfi_r128_LRA.append(None)
        lavfi_r128_LRA_low.append(None)
        lavfi_r128_LRA_high.append(None)
        lavfi_r128_true_peaks_ch0.append(None)
        lavfi_r128_true_peaks_ch1.append(None)

parsed.clear()
shortFrames = []
shortFrameCount = 1
for index, item in enumerate(lavfi_r128_used):
    if index % SHORT_FRAME_SIZE == 0:
        shortSum = 0
        if not item:
            skip=1
        else:
            skip=0
    else:
        if not item:
            skip=1
            continue
        shortSum += pow(10,lavfi_r128_M[index] / 20)
    if (index + 1) % SHORT_FRAME_SIZE == 0:
        if skip==1:
            shortFrames.append([shortFrameCount,None])
            shortFrameCount+=1
            continue
        shortFrameValue = 20 * math.log10(shortSum / SHORT_FRAME_SIZE)
        shortFrames.append([shortFrameCount,str(shortFrameValue)])
        shortFrameCount+=1
if len(lavfi_r128_used) % SHORT_FRAME_SIZE != 0:
    shortFrames.append([shortFrameCount,None])
with open(OUT_DIR+'\\sound_level.csv', 'w', newline='') as outFile:
    outCsvWriter = csv.writer(outFile, delimiter=';',quoting=csv.QUOTE_MINIMAL)
    outCsvWriter.writerows(shortFrames)

print("parsed")
# print(parsed)




# for filename in os.listdir(DIRECTORY):
#     if (filename.endswith(".mp4"): #or .avi, .mpeg, whatever.
#         os.system("ffmpeg -i {0} -f image2 -vf fps=fps=1 output%d.png".format(filename))
#     else:
#         continue