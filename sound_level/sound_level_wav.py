__author__ = 'mishninDY'
import os
import subprocess
import json
import math
import csv
import pprint
import logging
import time

class csvLog:
    def __init__(self,filename,mode = "w"):
        if mode.lower() == "w":
            if os.path.exists(filename):
                os.remove(filename)
        self.outFile = open(filename, 'w', newline='')
        self.outCsvWriter = csv.writer(self.outFile, delimiter='\t',quoting=csv.QUOTE_MINIMAL)
    def close(self):
        self.outFile.close()
    def __dell__(self):
        self.close()
    def add_row(self,row):
        self.outCsvWriter.writerow(row)
        self.outFile.flush()
    def add_rows(self,rows):
        self.outCsvWriter.writerows(rows)
        self.outFile.flush()


# print (os.getcwd())
FFMPEG_DIR="..\\FFMPEG\\BIN\\"
IN_DIR="../IN/"
OUT_DIR="../OUT"
r128_FRAME_DURATION=0.1
SHORT_FRAME_DURATION = 15
# CALC_TOTAL = 1
CALC_SHORT_FRAMES = 0
# LONG_FRAME_DURATION = SHORT_FRAME_DURATION*12 # 15*12=180s = 3 min
# SHORT_FRAME_SIZE=SHORT_FRAME_DURATION // r128_FRAME_DURATION
# LONG_FRAME_SIZE=LONG_FRAME_DURATION // r128_FRAME_DURATION
FILE_LIST = IN_DIR+"file_list.csv"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler(OUT_DIR+'/'+'sound_measure.log')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info('START with option CALC_SHORT_FRAMES={}'.format(CALC_SHORT_FRAMES))

shortFrames = []
total=[]
# rootdir = "D:\Полезное видео\GIT"
# rootdir = "H:\Полезное видео\Распознавание речи"
# rootdir = "D:\Полезное видео\Распознавание речи\cs224n 2017"
# rootdir = "\\\\ANDROID_6F6C\share\sda\sda1\cs224n 2017"
# rootdir = "L:\MGS-HNAS-FS-01.mgs.ru"
# rootdir = "H:\\test2"
rootdir = "\\\\MGS-HNAS-FS-01.mgs.ru\SAVFSZ_R"
totalLevelCSV = csvLog(OUT_DIR+'\\sound_level_total.csv')
totalLevelCSV.add_row(["lavfi_r128_I_total","lavfi_r128_LRA_total","lavfi_r128_LRA_low_total","lavfi_r128_LRA_high_total","lavfi_r128_true_peaks_ch0_total",
                       "totalDuration,inputFilePath"])

shortFrameLevelCSV = csvLog(OUT_DIR+'\\sound_level_frames.csv')
shortFrameLevelCSV.add_row(["lavfi_r128_I","lavfi_r128_LRA","lavfi_r128_LRA_low","lavfi_r128_LRA_high","lavfi_r128_true_peaks_ch0",
                           "t_start","t_finish","count","inputFilePath"])

if not os.path.exists(FILE_LIST):
    logger.error("file {} not found".format(FILE_LIST))
    exit(-1)
class dialect(csv.excel):
    delimiter = ';'
totalFileSizeOfList = 0
totalDurationOfList = 0
totalNumberOfFiles = 0
fileCount = 0
totalCalcTime =0
sizeOfProcessedFiles=0
durationOfProcessedFiles=0

with open (FILE_LIST, 'r') as fileList:
    fileListReader = csv.DictReader(fileList, dialect=dialect)
    for row in fileListReader:
        totalFileSizeOfList += int(row["size"])
        totalDurationOfList += int(row["duration"])
        totalNumberOfFiles += 1
per_file_t_start = time.clock()
with open (FILE_LIST, 'r') as fileList:
    fileListReader = csv.DictReader(fileList, dialect=dialect)
    for row in fileListReader:
        fileCount+=1
        unix_time = int(row["unix_time"])
        file_size = int(row["size"])
        duration = int(row["duration"])
        path = row["path"]
        inputFilePath = os.path.join(rootdir, path)
        sizeOfProcessedFiles += file_size
        durationOfProcessedFiles += duration
# for subdir, dirs, files in os.walk(rootdir):
#     for file in files:
#         filename, file_extension = os.path.splitext(file)
#         if  file_extension.lower() != ".mp4":
#             continue
#         inputFilePath=os.path.join(subdir, file)
#         logger.info('file: {}'.format(inputFilePath))
        logger.info('#{}/{}\t{:.1f}min\t{:.1f}Mb\tpath: {}'.format(fileCount,totalNumberOfFiles,duration/60,file_size/1000000, inputFilePath))
        #print(inputFilePath.encode('cp866', 'ignore'))

        # inputFilePath=inputFilePath.replace(r"\\",r"/")
        # inputFilePath=inputFilePath.replace(":",r"\\\\:")
        #inputFilePath="../IN/test.wav"
        # tmpFilePath=OUT_DIR+"/tmp.mkv"
        tmpFilePath=OUT_DIR+"/tmp.mp4"
        # tmpFilePath=OUT_DIR+"/tmp.wav"
        wavFilePath=OUT_DIR+"/inp.mp4"
        ffprobeLavfiStr="amovie={},ebur128=metadata=1:peak=true".format(inputFilePath.replace("\\",r"/").replace(":",r"\\:"))
        ffprobeLavfiStrTmp="amovie={},ebur128=metadata=1:peak=true".format(tmpFilePath.replace("\\",r"/").replace(":",r"\\:"))
        ffmpegFilterStr="ebur128=metadata=1:peak=true"
        try:
            # process = subprocess.Popen(["{}ffmpeg".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error","-y","-i",inputFilePath,"-vn", "-c","copy",tmpFilePath], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            process = subprocess.Popen(["{}ffmpeg".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error","-y","-i",inputFilePath,"-vn", "-c","copy",wavFilePath], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            process.wait()
            stdout = process.communicate()[0]
            stderr = process.communicate()[1]
            if len(stderr) != 0:
                logger.error(stderr.decode())
            inputFilePathSave = inputFilePath
            inputFilePath = wavFilePath
            # process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error",inputFilePath+"rrr" ,"-show_format", "-print_format", "json"], stdout=subprocess.PIPE)
            process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error",inputFilePath,"-show_format", "-print_format", "json"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            stdout = process.communicate()[0]
            stderr = process.communicate()[1]
            # print ('STDOUT:{}'.format(stdout))
            # print ('STDOUT:{} \n STDERR:{}'.format(stdout,stderr))
            if len(stderr) != 0:
                logger.error(stderr.decode())
            parsed =  json.loads(stdout)
            totalDuration=float(parsed["format"]["duration"])
            process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error", "-f", "lavfi","-i", ffprobeLavfiStr, "-show_frames","-show_format", "-print_format", "json"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            stdout = process.communicate()[0]
            stderr = process.communicate()[1]
            if len(stderr) != 0:
                logger.error(stderr.decode())
            # print ('STDOUT:{}'.format(stdout))
            parsed =  json.loads(stdout)
            process.wait()
            total=[]
            for frame in reversed(parsed["frames"]):
                if "tags" in frame:
                    lavfi_r128_I_total = float(frame["tags"]["lavfi.r128.I"])
                    lavfi_r128_LRA_total = float(frame["tags"]["lavfi.r128.LRA"])
                    lavfi_r128_LRA_low_total = float(frame["tags"]["lavfi.r128.LRA.low"])
                    lavfi_r128_LRA_high_total = float(frame["tags"]["lavfi.r128.LRA.high"])
                    lavfi_r128_true_peaks_ch0_total = float(frame["tags"]["lavfi.r128.true_peaks_ch0"])
                    # lavfi_r128_true_peaks_ch1_total = float(frame["tags"]["lavfi.r128.true_peaks_ch1"])
                    # total.append([lavfi_r128_I_total,lavfi_r128_LRA_total,lavfi_r128_LRA_low_total,lavfi_r128_LRA_high_total,lavfi_r128_true_peaks_ch0_total,lavfi_r128_true_peaks_ch1_total,
                    #               totalDuration,inputFilePath])
                    total.append([lavfi_r128_I_total,lavfi_r128_LRA_total,lavfi_r128_LRA_low_total,lavfi_r128_LRA_high_total,lavfi_r128_true_peaks_ch0_total,
                                  totalDuration,inputFilePathSave])
                    break
            totalLevelCSV.add_rows(total)
            t_start = 0
            t_finish = t_start +  SHORT_FRAME_DURATION
            count = 0
            ffmpegTime=0
            ffprobeTime=0
            while  t_finish <= totalDuration and CALC_SHORT_FRAMES == 1:
                t_ = time.clock()
                #process = subprocess.Popen(["{}ffmpeg".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error","-y","-i",inputFilePath,"-vn", "-ss",str(t_start),"-t",str(SHORT_FRAME_DURATION),"-c","copy",tmpFilePath], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                #process = subprocess.Popen(["{}ffmpeg".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error","-y","-i",inputFilePath, "-ss",str(t_start),"-t",str(SHORT_FRAME_DURATION),"-c","copy",tmpFilePath], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                #process = subprocess.Popen(["{}ffmpeg".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error","-y","-ss",str(t_start),"-i",inputFilePath,"-vn", "-t",str(SHORT_FRAME_DURATION),"-c","copy",tmpFilePath], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                process = subprocess.Popen(["{}ffmpeg".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error","-y","-ss",str(t_start),"-i",inputFilePath, "-t",str(SHORT_FRAME_DURATION),"-c","copy",tmpFilePath], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                process.wait()
                ffmpegTime += time.clock() - t_
                stdout = process.communicate()[0]
                stderr = process.communicate()[1]
                if len(stderr) != 0:
                    logger.error(stderr.decode())
                # print("ffmpeg:{}".format(process.wait()))
                t_ = time.clock()
                process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR),"-hide_banner", "-loglevel", "error", "-f", "lavfi","-i", ffprobeLavfiStrTmp,"-show_frames", "-show_format", "-print_format", "json"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                stdout = process.communicate()[0]
                stderr = process.communicate()[1]
                if len(stderr) != 0:
                    logger.error(stderr.decode())
                parsed =  json.loads(stdout)
                process.wait()
                ffprobeTime += time.clock() - t_
                # print("ffprobe:{}".format(process.wait()))
                for frame in reversed(parsed["frames"]):
                    if "tags" in frame:
                        lavfi_r128_I = float(frame["tags"]["lavfi.r128.I"])
                        lavfi_r128_LRA = float(frame["tags"]["lavfi.r128.LRA"])
                        lavfi_r128_LRA_low = float(frame["tags"]["lavfi.r128.LRA.low"])
                        lavfi_r128_LRA_high = float(frame["tags"]["lavfi.r128.LRA.high"])
                        lavfi_r128_true_peaks_ch0 = float(frame["tags"]["lavfi.r128.true_peaks_ch0"])
                        # lavfi_r128_true_peaks_ch1 = float(frame["tags"]["lavfi.r128.true_peaks_ch1"])
                        # shortFrames.append([lavfi_r128_I,lavfi_r128_LRA,lavfi_r128_LRA_low,lavfi_r128_LRA_high,lavfi_r128_true_peaks_ch0,lavfi_r128_true_peaks_ch1,
                        #                     t_start,t_finish,count,inputFilePath])
                        shortFrames.append([lavfi_r128_I,lavfi_r128_LRA,lavfi_r128_LRA_low,lavfi_r128_LRA_high,lavfi_r128_true_peaks_ch0,
                                            t_start,t_finish,count,inputFilePathSave])
                        break
                t_start = t_finish
                t_finish = t_start +  SHORT_FRAME_DURATION
                count+=1
                # print(count,t_start , t_finish)
            if CALC_SHORT_FRAMES == 1:
                logger.debug('ffmpeg/ffprobe execution time : {}'.format(ffmpegTime/ffprobeTime))

            totalCalcTime = time.clock()
            per_file_t_finish = totalCalcTime
            calcTime = per_file_t_finish - per_file_t_start
            per_file_t_start = time.clock()
            # print("per_file_t_finish={} per_file_t_start={}".format(per_file_t_finish, per_file_t_start))
            # remainTime = totalCalcTime*(totalFileSizeOfList/sizeOfProcessedFiles -1)
            remainTime = totalCalcTime*(totalDurationOfList/durationOfProcessedFiles -1)
            logger.info('calc. time {:.1f}min\ttotal calc. time {:.1f}min\tremain {:.1f}min'.format(calcTime/60,totalCalcTime/60,remainTime/60))
            shortFrameLevelCSV.add_rows(shortFrames)
        except:
            logger.exception("Somthing go wrang:")

shortFrameLevelCSV.close()
totalLevelCSV.close()
exit(0)




