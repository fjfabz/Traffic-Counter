import cv2
import numpy as np

def main():
    
    w = 800
    h = 600
    
    
    cap = cv2.VideoCapture('CarsDrivingUnderBridge.mp4')
    
    cap.set(3, w)
    cap.set(4, h)
    
#    print(cap.get(3))
#    print(cap.get(4))
    
    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    counter=0;

    i=0;
    while ret:
        
       # d = cv2.absdiff(frame1, frame2)
        blur=cv2.pyrMeanShiftFiltering(frame1,51,81)
        grey = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        #blur=cv2.medianBlur(grey,1)
       # blur = cv2.GaussianBlur(grey, (399,171), 0)
        
        ret, th = cv2.threshold( grey, 20, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
        dilated = cv2.dilate(th, np.ones((3, 3), np.uint8), iterations=1 )
        
        eroded = cv2.erode(dilated, np.ones((3, 3), np.uint8), iterations=1 )
        moments=cv2.moments(eroded,True);
        if moments['m00']>=1:
            x=int(moments['m10']/moments['m00'])
            y=int (moments['m01']/moments['m00'])
            if x>=0 and x<=640 and y==240:       #range of line coordinates for values on left lane
                i=i+1
                print(i)
           # elif x>102 and x<110 and y>105 and y<130: #range of line coordinatess for values on right lane
               # i=i+1
                #print(i)
            cv2.putText(frame1,'COUNT: %r' %i, (10,30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 2)
        img, c, h = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        cv2.drawContours(frame1, c, -1, (0, 0, 255), 2)
        cv2.line(frame1,(0,247),(640,247),5)
        cv2.line(frame1,(0,233),(640,233),5)
        for abc in c:
            cnt = abc
            x1,y1,w1,h1 = cv2.boundingRect(cnt)
            cv2.rectangle(frame1,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
            moments=cv2.moments(cnt)
            if moments['m00']>=1:
                x=int(moments['m10']/moments['m00'])
                y=int(moments['m01']/moments['m00'])
                if x>=0 and x<=640 and y>=237 and y<=242 :       #range of line coordinates for values on left lane
                    i=i+1
                    
           # elif x>102 and x<110 and y>105 and y<130: #range of line coordinatess for values on right lane
               # i=i+1
                #print(i)
                cv2.putText(frame1,'COUNT: %r' %i, (10,30), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 2)
        if counter>0:

            cv2.imshow("Original", frame2)
            cv2.imshow("Output", frame1)
        if cv2.waitKey(1) == 100: # exit on ESC
            break
        
        frame1 = frame2
        ret, frame2 = cap.read()
        counter=counter+1

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()
