import cv2
import mediapipe as mp
import numpy as np
import math
import pyttsx3
import pygame 
from pygame import mixer

mixer.init()
voice_left = mixer.Sound('left.wav')
voice_right = mixer.Sound('Right.wav')
voice_down = mixer.Sound('down.wav')
eyes_blink= mixer.Sound('eyes_blink.wav')
yawn = mixer.Sound('Yawning.wav')

counter_right=0
counter_down=0
counter_left=0
FONTS =cv2.FONT_HERSHEY_COMPLEX
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
LOWER_LIPS =[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
UPPER_LIPS=[ 185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78] 
BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHTBLUE = (180,130,70)
BLUE = (255,0,0)
RED = (0,0,255)
CYAN = (255,255,0)
YELLOW =(0,255,255)
MAGENTA = (255,0,255)
GRAY = (128,128,128)
GREEN = (0,255,0)
PURPLE = (128,0,128)
ORANGE = (0,165,255)
PINK = (147,20,255)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

def landmarksDetection(img, results, draw=False):
    img_height, img_width= img.shape[:2]
    mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
    if draw :
        [cv2.circle(img, p, 2, (0,255,0), -1) for p in mesh_coord]
    return mesh_coord

def euclaideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
    return distance

def blinkRatio(img, landmarks, right_indices, left_indices):
    # Right eyes 
    # horizontal line 
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    # vertical line 
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]
    # draw lines on right eyes 
    # cv.line(img, rh_right, rh_left, utils.GREEN, 2)
    # cv.line(img, rv_top, rv_bottom, utils.WHITE, 2)

    # LEFT_EYE 
    # horizontal line 
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]

    # vertical line 
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    rhDistance = euclaideanDistance(rh_right, rh_left)
    rvDistance = euclaideanDistance(rv_top, rv_bottom)

    lvDistance = euclaideanDistance(lv_top, lv_bottom)
    lhDistance = euclaideanDistance(lh_right, lh_left)
    
    if lvDistance != 0 and lhDistance !=0:
        reRatio = rhDistance/rvDistance
        leRatio = lhDistance/lvDistance
    
    ratio = (reRatio+leRatio)/2
    return ratio 


def MouthRatio(img, landmarks, top_indices, bottom_indices):

    lip_right = landmarks[bottom_indices[0]]
    lip_left = landmarks[bottom_indices[10]]

    lip_top = landmarks[top_indices[4]]
    lip_bottom = landmarks[bottom_indices[5]]

    
    lipDistance = euclaideanDistance(lip_top, lip_bottom)

    return lipDistance 


def colorBackgroundText(img, text, font, fontScale, textPos, textThickness=1,textColor=(0,255,0), bgColor=(0,0,0), pad_x=3, pad_y=3):
  
    (t_w, t_h), _= cv2.getTextSize(text, font, fontScale, textThickness) # getting the text size
    x, y = textPos
    cv2.rectangle(img, (x-pad_x, y+ pad_y), (x+t_w+pad_x, y-t_h-pad_y), bgColor,-1) # draw rectangle 
    cv2.putText(img,text, textPos,font, fontScale, textColor,textThickness ) # draw in text

    return img


Threshold_Frame = [200,350,450]
counter = 0
counter_eye = 0
counter_mouth = 0 
Counter_right=0
Counter_down=0
Counter_left=0
counter_left=0
counter_right=0
counter_down=0

while cap.isOpened():
    success, image = cap.read()

    # Flip the image horizontally for a later selfie-view display
    # Also convert the color space from BGR to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance
    image.flags.writeable = False
    
    # Get the result
    results = face_mesh.process(image)
    
    # To improve performance
    image.flags.writeable = True
    
    # Convert the color space from RGB to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    img_h, img_w, img_c = image.shape
    face_3d = []
    face_2d = []
   
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    if idx == 1:
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                    x, y = int(lm.x * img_w), int(lm.y * img_h)

                    # Get the 2D Coordinates
                    face_2d.append([x, y])

                    # Get the 3D Coordinates
                    face_3d.append([x, y, lm.z])       
            
            # Convert it to the NumPy array
            face_2d = np.array(face_2d, dtype=np.float64)

            # Convert it to the NumPy array
            face_3d = np.array(face_3d, dtype=np.float64)

            # The camera matrix
            focal_length = 1 * img_w

            cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                    [0, focal_length, img_w / 2],
                                    [0, 0, 1]])

            # The Distance Matrix
            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            # Solve PnP
            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            # Get rotational matrix
            rmat, jac = cv2.Rodrigues(rot_vec)

            # Get angles
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            # Get the y rotation degree
            x = angles[0] * 360
            y = angles[1] * 360


            if y< -10:
                text = "Looking Left"
                Counter_left += 1             

            if y > 10:
                text = "Looking Right"
                Counter_right += 1

            if x < -4:
                text = "Looking Down"
                Counter_down += 1
              
            else:
                text = "Looking Forward"
                
            if y< -10:
                Counter_right=0
                Counter_down=0
                Counter_forward=0
                counter_down=0
                counter_right=0
                if Counter_left % Threshold_Frame[counter_left] == 0  and pygame.mixer.get_busy()==0:
                    counter_left +=1
                    counter_left = counter_left % 3
                    if counter_left == 0:
                        Counter_left = 0
                    
                    voice_left.play()
            
            if  y > 10:
                Counter_left=0
                Counter_down=0
                Counter_forward=0
                counter_left=0
                counter_down=0
                if Counter_right > Threshold_Frame[counter_right] and pygame.mixer.get_busy()==0:
                    
                    counter_right +=1
                    counter_right = counter_right % 3  
                    
                    if counter_right == 0:
                        Counter_right = 0
                    
                    voice_right.play()
                    
       
            if x < -4:
                Counter_right=0
                Counter_left=0
                Counter_forward=0
                if Counter_down % Threshold_Frame[counter_down] == 0 and pygame.mixer.get_busy()==0:

                    counter_down +=1
                    counter_down = counter_down % 3  
                    
                    if counter_down == 0:
                        Counter_down = 0                    
                    voice_down.play()
              
            
            frame_height, frame_width= image.shape[:2] 
            
            if results.multi_face_landmarks:
                mesh_coords = landmarksDetection(image, results, False)
                ratio = blinkRatio(image, mesh_coords, RIGHT_EYE, LEFT_EYE)
                Mouth_dist= MouthRatio(image, mesh_coords, UPPER_LIPS, LOWER_LIPS)
                colorBackgroundText(image,  f'Eyes Clsoed for: {counter_eye} frames', FONTS, 0.6, (10,30),2, LIGHTBLUE, WHITE)
                colorBackgroundText(image,  f'Mouth Open for: {counter_mouth} frames', FONTS, 0.6, (350,30),2, LIGHTBLUE, WHITE)
                colorBackgroundText(image,  f'Seeing left for: {Counter_left} frames', FONTS, 0.6, (10,60),2, LIGHTBLUE, WHITE)
                colorBackgroundText(image,  f'Seeing right for: {Counter_right} frames', FONTS, 0.6, (350,60),2, LIGHTBLUE, WHITE)
                colorBackgroundText(image,  f'Seeing Down for : {Counter_down} frames', FONTS, 0.6, (10,90),2, LIGHTBLUE, WHITE)

                if ratio > 4.0:
                    counter_eye += 1
                    if counter_eye > 30 and pygame.mixer.get_busy()==0:
                        eyes_blink.play()
                        counter_eye = 0
                else: 
                    counter_eye=0
                if 45 < Mouth_dist:
                    counter_mouth += 1
                    if counter_mouth > 50 and pygame.mixer.get_busy()==0:
                        yawn.play()

                        counter_mouth = 0
                else: 
                    counter_mouth=0
    colorBackgroundText(image, 'Press Button Q to Quit', FONTS, 0.7, (200,460),2, LIGHTBLUE, WHITE)       
    cv2.imshow('Driver Alertness Estimation', image)

    key = cv2.waitKey(5) & 0xFF
    if key == ord("q"):
        break    

cap.release()
cv2.destroyAllWindows()