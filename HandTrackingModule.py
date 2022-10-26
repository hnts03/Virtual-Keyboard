import cv2
import mediapipe as mp          # for skeletal hand model
import time                     # for checking frame rate
import numpy as np

# Changes(10.25)
# 1. 2 New function added 
#       * handDetector.KNN(self, mode_on=True, data_path='./DataSet.txt) 
#           -> make knn model instance
#       * handDetector.KNN_result(self, hand_index=0) 
#           -> get result through knn model
# 2. 2 Existing function changed
#       * handDetector.findHands() 
#           -> new parameter makes drawing hand index under the 0-indexed lm position
#       * handDetector.findPosition() 
#           -> return all hand Landmarks


class handDetector():
    def __init__(self,
               static_image_mode=False,
               max_num_hands=2,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):

        self.mode = static_image_mode
        self.maxHands = max_num_hands
        self.complexity = model_complexity
        self.detectionCon = min_detection_confidence
        self.trackingCon = min_tracking_confidence

        self.mpHands = mp.solutions.hands    # get mp.solutions.hands module
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity,  # make Hands() class instance, use default
                                        self.detectionCon, self.trackingCon)        # for optimization, using non-static parameter                                                                                         
        self.mpDraw = mp.solutions.drawing_utils

        self.knn_isCreated = False
        

    def KNN(self, mode_on=True, data_path='./DataSet.txt'):
        file = np.genfromtxt(data_path, delimiter=',')
        angle = file[:,:-1].astype(np.float32)
        label = file[:, -1].astype(np.float32)
        self.knn = cv2.ml.KNearest_create()
        self.knn.train(angle, cv2.ml.ROW_SAMPLE, label)
        self.knn_isCreated = True


    def findHands(self, img, draw_hand_index=False):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                                    # mphands use only RGB images but cv2 images are BGR images.
                                    # So, it is necessary to convert

        self.results = self.hands.process(imgRGB)

        #print(results.multi_hand_landmarks)                # for checking hand position

        if self.results.multi_hand_landmarks:            
            for index, handLms in enumerate(self.results.multi_hand_landmarks):    # handLms is a single hand!
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)         # draw landmarks points and connections on img
                
                if draw_hand_index:
                    cv2.putText(img=img, text=str(index), 
                    org=(int(handLms.landmark[0].x * img.shape[1] - 10), int(handLms.landmark[0].y * img.shape[0] + 40)),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255,255,255), thickness=3)
        return img

    # def findPosition(self, img, realscale=False, windowsize=[], 
    #                     handNo=0, draw=False, scale_ratio=1, bias_ratio=0
    # ):                                                                  # 개선점 : 맨 처음에 탐지되던 손만 추적탐지하는것이 아니라 새로 탐지한 손의 handNo가 
    #                                                                     # 0번 인덱스가 되어서 손이 왔다갔다 하면 디텍팅이 안된다.
    #     lmList = []

    #     if self.results.multi_hand_landmarks:
    #         myHand = self.results.multi_hand_landmarks[handNo]
    #         for id, lm in enumerate(myHand.landmark):    # 0~20 landmarks
    #             #print(id)                               # id point
    #             #print(lm)                               # landmark position(x, y, z), These values are ratio

    #             if realscale:
    #                 cx, cy = int(lm.x*windowsize[0]*scale_ratio - windowsize[0]*bias_ratio), int(lm.y*windowsize[1]*scale_ratio - windowsize[1]*bias_ratio)
    #             else :
    #                 h, w, c = img.shape                      # get img's height, width, channel
    #                 cx, cy = int(lm.x*w), int(lm.y*h)        # get current x, y coordinate in integer               

    #             lmList.append([id, cx, cy])              # landmarks(0~20) are added to lmList consequently
    #             # print([id, cx, cy])                    # print coordinates and ids

    #             if draw: 
    #                 cv2.circle(img, (cx, cy), 8, (255, 255, 0), cv2.FILLED)
    #                 cv2.putText(img, str(id), (cx, cy-10), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3 )

    #     return lmList

    # lmList가 모든 손의 좌표를 반환하도록 설정함.
    def findPosition(self, img, realscale=False, windowsize=[], 
                        draw=False, scale_ratio=1, bias_ratio=0
    ):                                                                  # 개선점 : 맨 처음에 탐지되던 손만 추적탐지하는것이 아니라 새로 탐지한 손의 handNo가 
                                                                        # 0번 인덱스가 되어서 손이 왔다갔다 하면 디텍팅이 안된다.
        lmList = []

        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:
                temp = []
                for id, lm in enumerate(myHand.landmark):    # 0~20 landmarks
                    #print(id)                               # id point
                    #print(lm)                               # landmark position(x, y, z), These values are ratio

                    if realscale:
                        cx, cy = int(lm.x*windowsize[0]*scale_ratio - windowsize[0]*bias_ratio), int(lm.y*windowsize[1]*scale_ratio - windowsize[1]*bias_ratio)
                    else :
                        h, w, c = img.shape                      # get img's height, width, channel
                        cx, cy = int(lm.x*w), int(lm.y*h)        # get current x, y coordinate in integer               

                    temp.append([id, cx, cy])              # landmarks(0~20) are added to lmList consequently
                    # print([id, cx, cy])                    # print coordinates and ids

                    if draw: 
                        cv2.circle(img, (cx, cy), 8, (255, 255, 0), cv2.FILLED)
                        cv2.putText(img, str(id), (cx, cy-10), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3 )

                lmList.append(temp)

        return lmList

    def KNN_result(self, hand_index=0): # for One-hand landmarks 
        myHand = self.results.multi_hand_landmarks[hand_index]
        joint = np.zeros((21,3))
        for j, lm in enumerate(myHand.landmark):
            joint[j] = [lm.x, lm.y, lm.z]
        
        v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0,  9, 10, 11,  0, 13, 14, 15,  0, 17, 18, 19], :]
        v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :]

        v = v2 - v1
        v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

        compareV1 = v[[0, 1, 2, 4, 5, 6, 7,  8,  9, 10, 12, 13, 14, 16, 17], :]
        compareV2 = v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]

        angle = np.arccos(np.einsum('nt,nt->n', compareV1, compareV2))

        angle = np.degrees(angle)

        data = np.array([angle], dtype=np.float32)
        ret, results, neighbours, dist = self.knn.findNearest(data,3)
        key = int(results[0][0])
        
        return key

    
    

    # def drawLMcircle(self, img, landmarks, COLOR, ):
    #     cv2.cir

def __main():
    cap = cv2.VideoCapture(0)       # using 0 indexed webcam
    pTime = 0                       # previous time
    cTime = 0                       # current time
    detector = handDetector()
    isFlipped = True

    while True:
        success, img = cap.read()
        img = cv2.resize(img, (1280,720))
        if isFlipped:
            img = cv2.flip(img, 1)
        detector.findHands(img, draw_hand_index=True)
        detector.KNN()
        All_lmList = detector.findPosition(img)
        for index, lmList in enumerate(All_lmList):
            # if len(lmList) != 0:
            #     print(index)
            #     print(lmList[4])        # if you want landmark N's position, input N for the index
            print(f'{index} hand : {detector.KNN_result(hand_index=index)}')

        # --- Draw FPS rate ---
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)) + "FPS", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3 )

        # image
        cv2.imshow("Hand Tracking Image", img)    # run webcam
        # cv2.imshow("Original Image", ori_img)    # run webcam

        if cv2.waitKey(1) != -1:    # for realtime
            break


if __name__ == "__main__":
    __main()