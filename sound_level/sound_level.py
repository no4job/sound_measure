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
shortFrames = []
total=[]
rootdir = "D:\Полезное видео\GIT"
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if  file_extension.lower() != ".mp4":
            continue
        inputFilePath=os.path.join(subdir, file)

        print(inputFilePath.encode('cp866', 'ignore'))
        # inputFilePath=inputFilePath.replace(r"\\",r"/")
        # inputFilePath=inputFilePath.replace(":",r"\\\\:")
        #inputFilePath="../IN/test.wav"
        # tmpFilePath=OUT_DIR+"/tmp.mkv"
        tmpFilePath=OUT_DIR+"/tmp.mp4"
        ffprobeLavfiStr="amovie={},ebur128=metadata=1:peak=true".format(inputFilePath.replace("\\",r"/").replace(":",r"\\:"))
        ffprobeLavfiStrTmp="amovie={},ebur128=metadata=1:peak=true".format(tmpFilePath.replace("\\",r"/").replace(":",r"\\:"))
        ffmpegFilterStr="ebur128=metadata=1:peak=true"
        process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error",inputFilePath ,"-show_format", "-print_format", "json"], stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        #print ('STDOUT:{}'.format(stdout))
        parsed =  json.loads(stdout)
        totalDuration=float(parsed["format"]["duration"])
        process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error", "-f", "lavfi","-i", ffprobeLavfiStr, "-show_frames","-show_format", "-print_format", "json"], stdout=subprocess.PIPE)
        stdout = process.communicate()[0]
        #print ('STDOUT:{}'.format(stdout))
        parsed =  json.loads(stdout)
        for frame in reversed(parsed["frames"]):
            if "tags" in frame:
                lavfi_r128_I_total = float(frame["tags"]["lavfi.r128.I"])
                lavfi_r128_LRA_total = float(frame["tags"]["lavfi.r128.LRA"])
                lavfi_r128_LRA_low_total = float(frame["tags"]["lavfi.r128.LRA.low"])
                lavfi_r128_LRA_high_total = float(frame["tags"]["lavfi.r128.LRA.high"])
                lavfi_r128_true_peaks_ch0_total = float(frame["tags"]["lavfi.r128.true_peaks_ch0"])
                lavfi_r128_true_peaks_ch1_total = float(frame["tags"]["lavfi.r128.true_peaks_ch1"])
                total.append([lavfi_r128_I_total,lavfi_r128_LRA_total,lavfi_r128_LRA_low_total,lavfi_r128_LRA_high_total,lavfi_r128_true_peaks_ch0_total,lavfi_r128_true_peaks_ch1_total,
                              totalDuration,inputFilePath])
                break
        t_start = 0
        t_finish = t_start +  SHORT_FRAME_DURATION
        count = 0
        while  t_finish <= totalDuration:
            process = subprocess.Popen(["{}ffmpeg".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error","-y","-i",inputFilePath,"-vn", "-ss",str(t_start),"-t",str(SHORT_FRAME_DURATION),"-c","copy",tmpFilePath], stdout=subprocess.PIPE)
            print("ffmpeg:{}".format(process.wait()))
            process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error", "-f", "lavfi","-i", ffprobeLavfiStrTmp,"-show_frames", "-show_format", "-print_format", "json"], stdout=subprocess.PIPE)
            stdout = process.communicate()[0]
            #print ('STDOUT:{}'.format(stdout))
            parsed =  json.loads(stdout)
            print("ffprobe:{}".format(process.wait()))
            for frame in reversed(parsed["frames"]):
                if "tags" in frame:
                    lavfi_r128_I = float(frame["tags"]["lavfi.r128.I"])
                    lavfi_r128_LRA = float(frame["tags"]["lavfi.r128.LRA"])
                    lavfi_r128_LRA_low = float(frame["tags"]["lavfi.r128.LRA.low"])
                    lavfi_r128_LRA_high = float(frame["tags"]["lavfi.r128.LRA.high"])
                    lavfi_r128_true_peaks_ch0 = float(frame["tags"]["lavfi.r128.true_peaks_ch0"])
                    lavfi_r128_true_peaks_ch1 = float(frame["tags"]["lavfi.r128.true_peaks_ch1"])
                    shortFrames.append([lavfi_r128_I,lavfi_r128_LRA,lavfi_r128_LRA_low,lavfi_r128_LRA_high,lavfi_r128_true_peaks_ch0,lavfi_r128_true_peaks_ch1,
                                        t_start,t_finish,count,inputFilePath])
                    break
            t_start = t_finish
            t_finish = t_start +  SHORT_FRAME_DURATION
            count+=1
            print(count,t_start , t_finish)
with open(OUT_DIR+'\\sound_level_total.csv', 'w', newline='') as outFile:
    fieldnames = ["lavfi_r128_I_total","lavfi_r128_LRA_total","lavfi_r128_LRA_low_total","lavfi_r128_LRA_high_total","lavfi_r128_true_peaks_ch0_total",
                  "lavfi_r128_true_peaks_ch1_total","totalDuration,inputFilePath"]
    outCsvWriter = csv.writer(outFile, delimiter=';',quoting=csv.QUOTE_MINIMAL)
    outCsvWriter.writerow(fieldnames)
    outCsvWriter.writerows(total)
with open(OUT_DIR+'\\sound_level.csv', 'w', newline='') as outFile:
    fieldnames = ["lavfi_r128_I","lavfi_r128_LRA","lavfi_r128_LRA_low","lavfi_r128_LRA_high","lavfi_r128_true_peaks_ch0","lavfi_r128_true_peaks_ch1",
                  "t_start","t_finish","count","inputFilePath"]
    outCsvWriter = csv.writer(outFile, delimiter=';',quoting=csv.QUOTE_MINIMAL)
    outCsvWriter.writerow(fieldnames)
    outCsvWriter.writerows(shortFrames)
exit(0)
