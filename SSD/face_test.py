from facenet_pytorch import MTCNN, InceptionResnetV1

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
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.FaceDetectionModule import FaceDetector
import cvzone
import mediapipe as mp
import math

mesh_detector = FaceMeshDetector()
detector = FaceDetector(minDetectionCon=0.8)

save = False
setting = False
track = False

from serial import Serial
mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)
resnet = InceptionResnetV1(pretrained="vggface2").eval()

#serialPort = '/dev/cu.usbmodem145301'
#baudRate = 9600
#ser = Serial(serialPort, baudRate, timeout = 0.5)
#x2 = b"1"

net = build_ssd('test', 300, 21)    # initialize SSD
net.load_weights('ssd300_mAP_77.43_v2.pth')
transform = BaseTransform(net.size, (104/256.0, 117/256.0, 123/256.0))
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75)

def vector_2d_angle(v1, v2):  # 求出v1,v2兩條向量的夾角
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos(
            (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 100000.
    return angle_


def hand_angle(hand_):
    angle_list = []
    # ---------------------------- thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- 食指上下方向
    angle_ = vector_2d_angle(
        ((int(hand_[23][0]) - int(hand_[21][0])), (int(hand_[23][1]) - int(hand_[21][1]))),  #→
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)
    # ---------------------------- 食指左右方向
    angle_ = vector_2d_angle(
        ((int(hand_[22][0]) - int(hand_[21][0])), (int(hand_[22][1]) - int(hand_[21][1]))),  #→
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)
    return angle_list


def hand_gesture(angle_list):  # 偵測手勢
    if 100000. not in angle_list:
        if ((10<angle_list[0]<30) or (angle_list[0]>40)) and (angle_list[1]<40) and (angle_list[2]>100) and (angle_list[3]>100) and (angle_list[4]>40) and (angle_list[5]<30):
            print("up")

        if ((10<angle_list[0]<30) or (angle_list[0]>40)) and (angle_list[1]<40) and (angle_list[2]>100) and (angle_list[3]>100) and (angle_list[4]>40) and (angle_list[5]>150):
            print("down")

        if ((10<angle_list[0]<30) or (angle_list[0]>40)) and (angle_list[1]<40) and (angle_list[2]>100) and (angle_list[3]>100) and (angle_list[4]>40) and (angle_list[6]<30):
            print("left")

        if ((10<angle_list[0]<30) or (angle_list[0]>40)) and (angle_list[1]<40) and (angle_list[2]>100) and (angle_list[3]>100) and (angle_list[4]>40) and (angle_list[6]>150):
            print("right")


def face_svae(frame):
    face, prob = mtcnn(frame, return_prob = True)
    if face is not None and prob > 0.8:
        emb = resnet(face.unsqueeze(0))
        print(emb)
        return emb
    else:
        return

def detect(frame, net, transform, emb_p):
    height, width = frame.shape[:2]
    frame_t = transform(frame)[0]
    x = torch.from_numpy(frame_t).permute(2, 0, 1)
    x = Variable(x.unsqueeze(0))
    y = net(x)
    detections = y.data
    scale = torch.Tensor([width, height, width, height])
    # detections = [batch, number of classes, number of occurence, (score, x0, Y0, x1, y1)]
    for i in range(detections.size(1)):
        j = 0
        while detections[0, i, j, 0] >= 0.6:
            pt = (detections[0, i, j, 1:] * scale).numpy()
            if labelmap[i - 1] == 'person':
                print(labelmap[i - 1])
                img = frame[int(pt[1]):int(pt[1])+int(pt[3]), int(pt[0]):int(pt[0])+int(pt[2])]
                print('img:',img)
                if img != []:
                    img_d, faces = detector.findFaces(img, draw=True)
                    print('img_d:',img_d)
                    if faces != []:
                        print('faces:',faces)
                        (x, y, w, h) = faces[0]['bbox']
                        face_d = img[y-10:y + h+10, x-10:x + w+10]
                        print('face_d:',face_d)
                        if face_d != []:
                            cv2.imshow('face_d', face_d)
                            face, prob = mtcnn(face_d, return_prob = True)
                            print('face:',face)
                            if face is not None:
                                emb = resnet(face.unsqueeze(0))
                                dist = torch.dist(emb, emb_p)
                                print('dist:', dist)
                                if dist < 1:
                                    img_mesh, faces_mesh = mesh_detector.findFaceMesh(face_d, draw=True)
                                    # img_mesh, faces_mesh = mesh_detector.findFaceMesh(img, draw=True)
                                    #print("face_mesh",faces_mesh)
                                    if faces_mesh != []:
                                        face = faces_mesh[0]
                                        pointLeft = face[145]
                                        pointLeft = [pointLeft[0]+x-10,pointLeft[1]+y-10]
                                        pointRight = face[374]
                                        pointRight = [pointRight[0] + x-10, pointRight[1] + y-10]
                                        cv2.circle(frame, pointLeft, 5, (255,0,255), cv2.FILLED)
                                        cv2.circle(frame, pointRight, 5, (255,0,255), cv2.FILLED)
                                        cv2.line(frame, pointLeft, pointRight, (0,200,0), 3)
                                        w_, _ = mesh_detector.findDistance(pointLeft, pointRight)
                                        W = 6.3
                                        #Focal Length
                                        f = 1000
                                        #Finding Distance

                                        d = (W*f)/w_
                                        print(d)

                                        #printtext
                                        cvzone.putTextRect(frame, f'Depth: {int(d)}cm', (face[10][0]-100+x, face[10][1]-50+y), scale = 2)
                                    results = hands.process(img)

                                    if results.multi_hand_landmarks:
                                        for hand_landmarks in results.multi_hand_landmarks:
                                            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                                            keypoint_pos = []
                                            for i in range(21):
                                                x = hand_landmarks.landmark[i].x * frame.shape[1]
                                                y = hand_landmarks.landmark[i].y * frame.shape[0]
                                                keypoint_pos.append((x, y))
                                            keypoint_pos.append((0, 0))
                                            keypoint_pos.append((1, 0))   #→
                                            keypoint_pos.append((0, 1))   #↓
                                            if keypoint_pos:
                                                # 得到各手指的夾角資訊
                                                angle_list = hand_angle(keypoint_pos)
                                                # 根據角度判斷此手勢是否為愛心
                                                hand_gesture(angle_list)
                                    cv2.imshow('MediaPipe Hands', frame)
                #ser.write(x2)
                #cv2.rectangle(frame, (int(pt[0]), int(pt[1])), (int(pt[2]), int(pt[3])), (255, 0, 0), 2)
                #cv2.putText(frame, labelmap[i - 1], (int(pt[0]), int(pt[1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            j += 1
    return frame

video_capture = cv2.VideoCapture(0)

while True:
    _, frame = video_capture.read()
    if not save:
        embs_people = face_svae(frame)
        if embs_people is not None:
            save = True
    if (save):
        canvas = detect(frame, net, transform, embs_people)
        cv2.imshow('Video', canvas)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()





