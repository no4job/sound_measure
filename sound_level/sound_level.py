__author__ = 'mishninDY'
import os
import subprocess
import json
import pprint
print (os.getcwd())
FFMPEG_DIR="..\\FFMPEG\\BIN\\"
IN_DIR="../IN/"


# os.system("{0}ffprobe -hide_banner -loglevel panic -f lavfi amovie={1}test.wav,ebur128=metadata=1:peak=true "
#           "-show_frames -show_format "
#           "-print_format json".format(FFMPEG_DIR,IN_DIR))


# process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR), "-hide_banner -loglevel panic -f lavfi amovie={"
#                                                             "}test.wav,ebur128=metadata=1:peak=true -show_frames -show_format -print_format json".format(IN_DIR)], stdout=subprocess.PIPE,shell=True)

process = subprocess.Popen(["{}ffprobe".format(FFMPEG_DIR), "-f", "lavfi","-i", "amovie=../in/test.wav,ebur128=metadata=1:peak=true","-show_frames", "-show_format", "-print_format", "json"], stdout=subprocess.PIPE,shell=True)
stdout = process.communicate()[0]
print ('STDOUT:{}'.format(stdout))
parsed =  json.loads(stdout)
print ("Parsed")
# print(parsed)


# for filename in os.listdir(DIRECTORY):
#     if (filename.endswith(".mp4"): #or .avi, .mpeg, whatever.
#         os.system("ffmpeg -i {0} -f image2 -vf fps=fps=1 output%d.png".format(filename))
#     else:
#         continue