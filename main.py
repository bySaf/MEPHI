from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
from datetime import datetime
from SORT import *
import threading
import uvicorn
import asyncio
import numpy as np
import socket
import math
import cv2
import os
from db import DataBase

app = FastAPI()
app.mount(
    "/aboba",
    StaticFiles(directory='static'),
    name="static",
)

templates = Jinja2Templates(directory="templates")

camera = cv2.VideoCapture("aboba.mp4")
#cap = cv2.VideoCapture('rtsp://admin:Sirius_2024@192.168.1.64/:8080/stream1')

model = YOLO("best.pt")

tracker = Sort(max_age=10, min_hits=3, iou_threshold=0.3)
timer = [0.0 for _ in range(1000)]
checker = 0
check = False
tim = None


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def get_stream(websocket: WebSocket):
    global timer, tracker, checker, check

    await websocket.accept()
    try:

        while True:

            flag, img = camera.read()

            if check:

                results = model.predict(img, stream=True, verbose=False)

                detections = np.empty((0, 5))

                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = math.ceil((box.conf[0] * 100)) / 100
                        currentArray = np.array([x1, y1, x2, y2, conf])
                        detections = np.vstack((detections, currentArray))

                resultsTracker = tracker.update(detections)

                for result in resultsTracker:
                    x1, y1, x2, y2, Id = map(int, result)
                    current = datetime.now().timestamp()
                    if timer[Id] == 0.0:
                        timer[Id] = current
                    past = int(current - timer[Id])
                    color = (0, 255, 0)
                    if past >= 0.5:
                        color = (0, 255, 255)
                    if past >= 1:
                        color = (0, 0, 255)
                        print(f"коптер эээээээщщщщщщкереееее!!!")
                        if checker == 0:
                            path = r'C:\Users\Sirius\PycharmProjects\pythonProject\saves'
                            name = f'{DataB.get_name_of_incident(tim)}.jpg'
                            full = os.path.join(path, name)
                            cv2.imwrite(full, img)
                            DataB.update_data_of_incident(full, tim)
                            time_of_detection = datetime.now()
                            DataB.update_time_of_incident(time_of_detection.now(), tim)
                            checker = 1

                    cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                    cv2.putText(img, str(past), (x1 + 5, y1 + 50), cv2.FONT_ITALIC, 2, (213, 155, 246),
                                5)

            ret, buffer = cv2.imencode('.jpg', img)

            if not ret:
                continue

            await websocket.send_bytes(buffer.tobytes())

            await asyncio.sleep(0.03)


    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")


def start_socket_server():
    global check, tim
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 65432))
    server_socket.listen(5)

    print("Socket server started and listening on port 65432")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        message = client_socket.recv(1024).decode('utf-8')
        print(f"Received message: {message}")
        if message:
            check = True
            now = datetime.now()
            dat = now.date()
            tim = now.time()
            DataB.add_incident(message, dat, tim)
            print(now.date())
            print(now.time())

        client_socket.close()


@app.on_event("startup")
async def startup_event():
    socket_thread = threading.Thread(target=start_socket_server)
    socket_thread.daemon = True
    socket_thread.start()


if __name__ == '__main__':
    DataB = DataBase()
    uvicorn.run(app, host='localhost', port=8000)
