import os
import cv2
import time
import numpy as np

import VideoUtils
import HOG
import RawImage

video_name='/home/zhex/work/data/videos/30.mp4'
picture_path = '/home/zhex/work/data/pictures/30/'
video_cap = cv2.VideoCapture(video_name)

frame_count = 0
index = []

#  HOG不同距离度量 不同阈值
# Threshold_mse = 0.000167
Threshold = 0.000167

dist_metric = 'mse'

starttime = time.time()
while(video_cap.isOpened()):
    ret, _ = video_cap.read()
    if ret is False:
        break
    frame_count = frame_count + 1
print(frame_count)

frames = VideoUtils.get_all_frames(frame_count, video_name, 0, 1,)
length = len(frames)
print('length=',length)

for i in range(1,length,4):
    frame_x = frames[i-1]
    frame_x = np.array(frame_x)
    hog_x = HOG.compute_feature(frame_x,10)

    frame_x_delay = frames[i]
    frame_x_delay = np.array(frame_x_delay)
    hog_x_delay = HOG.compute_feature(frame_x_delay,10)

    distance = RawImage.get_distance_fn(dist_metric,hog_x,hog_x_delay)
    if distance > Threshold:
        index.append(i)

print('length_frame=',len(index))
# 抽取视频帧保存为图片
#需要重新打开视频流文件

video_cap0 = cv2.VideoCapture(video_name)
i = 0
j =0

while(True):
    ret,frame = video_cap0.read()
    if ret is False:
        break
    if i in index:
        j =  j+1
        cv2.imwrite(picture_path + str(j)+'.jpg',frame)
    i = i+ 1

# 图片合成视频
def pic2video(path):
    size = (1920,1080)
    filelist = os.listdir(path)
    filelist.sort(key=lambda x:int(x[:-4]))
    fps = 12
    file_path = "./"+ 'new' + ".mp4"
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter( file_path, fourcc, fps, size )
    for item in filelist:
        if item.endswith('.jpg'):
            item = path + item
            img =cv2.imread(item)
            video.write(img)
    video.release()
# pic2video(picture_path)

endtime = time.time()
print('time_total=',(endtime - starttime))