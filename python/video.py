'''
Author: ZHAO qinglingzhiqing@126.com
Date: 2025-10-01 09:50:11
LastEditors: ZHAO qinglingzhiqing@126.com
LastEditTime: 2025-10-01 11:43:43
FilePath: \python\video.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import cv2
from ultralytics import YOLO
# Load a pretrained YOLO11n model
model = YOLO("yolo11n.pt")
# cap = cv2.VideoCapture("http://192.168.1.111:81/stream")
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    results=model(img)
    for r in results:
        boxes=r.boxes
        for box in boxes:
            x1,y1,x2,y2=box.xyxy[0]
            x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            conf=box.conf[0]
            cls=int(box.cls[0])
            cv2.putText(img,f'{model.names[cls]} {conf:.2f}',(x1,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break