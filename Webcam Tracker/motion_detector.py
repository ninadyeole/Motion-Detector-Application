import cv2, time, pandas
from datetime import datetime

first_frame = None 
status_list = [None,None]
times = []
df = pandas.DataFrame(columns=["Start","End"])

video = cv2.VideoCapture(0)


while True :
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)


    if first_frame is None :
        first_frame = gray 
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 20, 255, cv2.THRESH_BINARY)[1] 
    
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contours in cnts :
        if cv2.contourArea(contours) < 1000 :
            continue
        status = 1
        (x,y,w,h) = cv2.boundingRect(contours)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), ) 

    if status_list[-1]==0 and status_list[-2]==1 :
        times.append(datetime.now())

    if status_list[-1]==1 and status_list[-2]==0 :
        times.append(datetime.now())        

    status_list.append(status)
    cv2.imshow("Capturing", gray)
    cv2.moveWindow("Capturing", 0, 0)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.moveWindow("Delta Frame", 768, 0)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.moveWindow("Threshold Frame", 0, 384)
    cv2.imshow("Color Frame", frame)
    cv2.moveWindow("Color Frame", 768, 384)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status==1 :
            times.append(datetime.now())
        break


for i in range (0,len(times),2):
    df = df.append({ "Start":times[i],"End":times[i+1] }, ignore_index=True )

df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows
