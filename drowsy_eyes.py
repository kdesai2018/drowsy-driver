#!/usr/bin/env python3

# imports
import face_recognition
import cv2
import time
from scipy.spatial import distance as dist
import vlc
import keyboard as kb

import googlemaps
from datetime import datetime





def main():
    closed_count = 0
    video_capture = cv2.VideoCapture(0)

    ret, frame = video_capture.read(0)
    # cv2.VideoCapture.release()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame)
    process = True

    song = vlc.MediaPlayer('wakeup_loop.mp3')

    while True:
        ret, frame = video_capture.read(0)

        # get it into the correct format
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        # get the correct face landmarks
        
        if process:
            face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame)

            # put something here
            for face_landmark in face_landmarks_list:
                left_eye = face_landmark['left_eye']
                right_eye = face_landmark['right_eye']


                color = (255,0,0)
                thickness = 2

                cv2.rectangle(small_frame, left_eye[0], right_eye[-1], color, thickness)

                cv2.imshow('Video', small_frame)
                cv2.waitKey(1)

                ear_left = get_ear(left_eye)
                ear_right = get_ear(right_eye)

                closed = ear_left < 0.2 and ear_right < 0.2

                if (closed):
                    closed_count += 1

                else:
                    closed_count = 0


                if (closed_count >= 10):
                    print('wake up')
                    song.play()
                    asleep = True
                    while (asleep): #continue this loop until they wake up and acknowledge music
                        song.play()
                        time.sleep(5)
                        song.stop() 
                        print(asleep)
                        if (kb.is_pressed('space')):
                            asleep = False
                            google_directions()
                        
                    closed_count = 0
                
        process = not process

def google_directions():
    with open('apikey.txt') as f:
        api_key = f.readline()
        f.close
    gclient = googlemaps.Client(key=api_key)



    now = datetime.now()

    origin = 30.288299,-97.735608
    dest = 30.282771,-97.736878

    directions_result = gclient.directions(origin,dest,mode="driving", departure_time=now)

    # directions = json.loads(directions_result)
    print(directions_result)

    
def get_ear(eye):

	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
 
	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])
 
	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)
 
	# return the eye aspect ratio
	return ear

if __name__ == "__main__":
    main()

