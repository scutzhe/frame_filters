import os
import cv2
import time
import numpy as np

import VideoUtils
import RawImage

video_name='/home/zhex/work/data/videos/30.mp4'
picture_path = '/home/zhex/work/data/pictures/30/'
video_cap = cv2.VideoCapture(video_name)

frame_count = 0
index = []
size = 4 #跳帧步数
# raw不同距离度量 不同阈值
# Threshold_mse = 0.168564367749
Threshold = 0.168564367749
dist_metric = 'mse'

starttime = time.time()

while(video_cap.isOpened()):
    ret,_ = video_cap.read()
    if ret is False:
        break
    frame_count = frame_count + 1

frames = VideoUtils.get_all_frames(frame_count, video_name, 0, 1,)
# length = len(frames)
# print('length=',length)
# print('frames = ',frames)
frames = np.array(frames)
# print(frames.shape)
# print(np.mean(frames,axis=0))

# # 方法一： 前后两帧之间逐一比较
# for i in range(1,length,4):
#     frame_x = frames[i-1]
#     frame_x = np.array(frame_x)
#     raw_x = RawImage.compute_feature(frame_x)
#
#     frame_x_delay = frames[i]
#     frame_x_delay = np.array(frame_x_delay)
#     raw_x_delay = RawImage.compute_feature(frame_x_delay)
#
#     distance = RawImage.get_distance_fn(dist_metric,raw_x,raw_x_delay)
#     if distance > Threshold:
#         index.append(i)
#
# # 方法二： 基准帧，超参，后面提取帧一次跟基准帧比较
# for i in range(1,length,4):
#     frame_0 = 100 # 先写一个值
#     frame = frames[i-1]
#     frame = np.array(frame)
#     raw = RawImage.compute_feature(frame)
#
#     distance = RawImage.get_distance_fn(dist_metric,raw,raw_0)
#     if distance > frame_0:
#         index.append(i)

# 方法三： 均值帧，自动化提取，后面的帧依次跟均值帧比较
# for i in range(1,length,size):
#     raw_avg = 100 #先写一个值
#     frame_0 = frames[i-1]
#     frame_0 = np.array(frame_0)
#     raw_0 = RawImage.compute_feature(frame_0)
#
#     distance = RawImage.get_distance_fn(dist_metric,raw_avg,raw_0)
#     if distance > Threshold:
#         index.append(i)
#
# print('length_index = ',len(index))
# 抽取视频帧保存为图片
#需要重新打开视频流文件
# video_cap0 = cv2.VideoCapture(video_name)
# i = 0
# j =0

# while(True):
#     ret,frame = video_cap0.read()
#     if ret is False:
#         break
#     if i in index:
#         j =  j+1
#         cv2.imwrite(picture_path + str(j)+'.jpg',frame)
#     i = i+ 1

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
pic2video(picture_path)

endtime = time.time()
print('time_total=',(endtime - starttime))

