#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 23:36:19 2021

@author: ray
"""

import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
import numpy as np
import cv2
if torch.cuda.is_available():
    torch.set_default_tensor_type('torch.cuda.FloatTensor')
from ssd import build_ssd
from data import BaseTransform, VOC_CLASSES as labelmap
import cv2

#from serial import Serial
#mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)
#resnet = InceptionResnetV1(pretrained="vggface2").eval()

#serialPort = '/dev/cu.usbmodem145301'
#baudRate = 9600
#ser = Serial(serialPort, baudRate, timeout = 0.5)
#x2 = b"1"


def detect(frame):
    net = build_ssd('test', 300, 21)    # initialize SSD
    net.load_weights('/Users/ray/Desktop/Auto_labelimg/SSD/ssd300_mAP_77.43_v2.pth')
    transform = BaseTransform(net.size, (104/256.0, 117/256.0, 123/256.0))
    height, width = frame.shape[:2]
    frame_t = transform(frame)[0]
    x = torch.from_numpy(frame_t).permute(2, 0, 1)
    x = Variable(x.unsqueeze(0))
    y = net(x)
    detections = y.data
    list = []
    scale = torch.Tensor([width, height, width, height])
    # detections = [batch, number of classes, number of occurence, (score, x0, Y0, x1, y1)]
    for i in range(detections.size(1)):
        j = 0
        while detections[0, i, j, 0] >= 0.6:
            pt = (detections[0, i, j, 1:] * scale).numpy()
            item = [int(pt[0]), int(pt[1]), int(pt[2]), int(pt[3]), labelmap[i - 1]]
            #obj = PascalObject(labelmap[i - 1], "Unspecified", truncated=False, difficult=False, bndbox=BndBox(int(pt[0]), int(pt[1]), int(pt[2]), int(pt[3])))
            list.append(item)
            if labelmap[i - 1] == 'person':
                print(labelmap[i - 1])

            #cv2.rectangle(frame, (int(pt[0]), int(pt[1])), (int(pt[2]), int(pt[3])), (255, 0, 0), 2)
            #cv2.putText(frame, labelmap[i - 1], (int(pt[0]), int(pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            j += 1
    #pascal_ann = PascalVOC("1.jpg", size=size_block(w, h, c), objects=list, path='/Users/ray/Desktop/robot-vision_final_porject/image/1.jpg', folder='image')
    #pascal_ann.save("/Users/ray/Desktop/robot-vision_final_porject/annotation/10.xml")
    return list

#video_capture = cv2.VideoCapture(0)
'''
img = cv2.imread('/Users/ray/Desktop/robot-vision_final_porject/image/2.jpg')
h, w, c = img.shape
canvas = detect(img)
print(canvas)
#video_capture.release()
cv2.destroyAllWindows()

'''



