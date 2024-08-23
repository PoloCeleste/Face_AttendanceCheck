import cv2 as cv
import os, schedule
from datetime import datetime
import numpy as np
from tkinter import *

detector = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv.face.LBPHFaceRecognizer_create()
font = cv.FONT_HERSHEY_SIMPLEX
today = datetime.today().strftime("%Y-%m-%d")

def top(contents='', size=50, Delay=3000):
    top = Tk()
    Message(top, text=contents, font=("times", size, "bold"), padx=200, pady=300).pack()
    top.after(Delay, top.destroy)
    top.mainloop()


def faceDetect():
	cap = cv.VideoCapture(0)
	cap.set(3,1920)
	cap.set(4,1080)

	while True:
		_,img = cap.read()
		gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
		faces = detector.detectMultiScale(
			gray,
			scaleFactor=1.2,
			minNeighbors=5,
			minSize=(20, 20)
			)
		for (x,y,w,h) in faces:
			cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
		cv.imshow('faceDetect',img)
		k = cv.waitKey(30) & 0xff
		if k == 27:
			break

	cap.release()
	cv.destroyAllWindows()


def makeDataset():
    cam = cv.VideoCapture(0)
    cam.set(3, 1920)
    cam.set(4, 1080)
    f = open("Regist.txt", "r")
    names = []
    while True:
        line = f.readline().strip()
        if not line: break
        names.append(line)
    f.close()
    face_id = len(names)
    print("\n Look the camera and wait")
    count = 0
    while(True):
        ret, img = cam.read()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)
        for (x,y,w,h) in faces:
            cv.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            count += 1

            cv.imwrite("dataset/User." + str(face_id) + '.'+str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv.imshow('image',img)
        k=cv.waitKey(100) & 0xff
        if k == 27:
            break
        elif count >= 70:
            break

    print("\n Exiting...")
    cam.release()
    cv.destroyAllWindows()


def getImagesAndLabels(path):
    from PIL import Image
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples,ids

def trainingData():
    path = 'dataset'    
    print ("\n Training faces. Wait")
    Faces, ids = getImagesAndLabels(path)
    recognizer.train(Faces, np.array(ids))
    recognizer.write('training/trainer.yml')
    print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))


def faceRecog():
    recognizer.read('training/trainer.yml')
    id = 0
    chancount=0
    jincount=0
    f = open("Regist.txt", "r")
    names = []
    while True:
        line = f.readline().strip()
        if not line: break
        names.append(line)
    f.close()
    counts=[]
    for x in range(len(names)):
        counts.append(x,0)

    cam = cv.VideoCapture(0)
    cam.set(3, 1920)
    cam.set(4, 1080)

    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    while True:
        _, img =cam.read()
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        
        faces = detector.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )

        for(x,y,w,h) in faces:
            cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, minScore = recognizer.predict(gray[y:y+h,x:x+w])
            if (minScore < 100):
                id = names[id]
                confidence = int(round(100 - minScore))
                for i in range(len(names)):
                    if (id == names[i]):
                        if (confidence  > 50):
                            if (counts[i] < 1):
                                chtime = datetime.now().strftime('%H:%M:%S')
                                top(str(id))
                                counts.append(i, 1)
                                print(f'{str(id)} Check-In ({chtime})')
                                break
                if (id == names[1]):
                    if (confidence  > 50):
                        if (chancount < 1):
                            chtime = datetime.now().strftime('%H:%M:%S')
                            top(str(id))
                            chancount += 1
                            print(f'{str(id)} Check-In ({chtime})')
                            break
                if (id == names[2]):
                    if (confidence  > 50):
                        if (jincount < 1):
                            top(str(id))
                            jincount += 1
                            break
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))

            
            
            cv.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
            
        chtime = datetime.now().strftime('%H:%M:%S')
        cv.putText(img, chtime, (0, 50), 3, 2, (155,200,230), 2)
        cv.imshow('faceRecog',img)
        
        k = cv.waitKey(10) & 0xff
        if k == 27:
            break

    print("\n Exiting Face_Recognition")
    cam.release()
    cv.destroyAllWindows()


def switch_case(num):
    if num=='0':
        faceDetect()
        return
    elif num=='1':
        makeDataset()
        return
    elif num=='2':
        trainingData()
        return
    elif num=='3':
        faceRecog()
        return
    else:
        print('\n다시 선택해주세요.\n')
        return


if __name__ == '__main__':
    num=''
    while(1):
        num=input('\n모드를 선택하세요. ( 0. 얼굴 인식 1. 데이터셋 추가 2. 데이터셋 학습 3. 학습된 얼굴 인식 4. 종료 ) : ')
        if num=='4':
            print('프로그램을 종료합니다.')
            break
        switch_case(num)

