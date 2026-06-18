#!/usr/bin/python3

import time
import io
import logging
import socketserver
import threading
import cv2
from http import server
from threading import Condition

# Customizable:
portNum = 7000 # Which port number the livestream will be streamed to  (e.g. 8000 means you can access the livestream from http://192.168.1.92:8000 if your IPv4 is 192.168.1.92)
streamWidth = 1080 # Width, in pixels, of the livestream
streamHeight = round(streamWidth * 9/16) # You can also change this value if you want different proportions
cameraIndex = 0 # Usually 0 for the first USB camera plugged in
HTML = "<html><head><title>Pivestream</title><style>body{margin:0;background-color:black}</style></head><body><img src='live.mjpg' width='100%'/></body></html>"

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()
    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stop':
            self.server.shutdown()
            return
        if self.path == '/snap.jpg':
            with output.condition:
                output.condition.wait()
                if output.frame is not None:
                    self.send_response(200)
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(output.frame))
                    self.end_headers()
                    self.wfile.write(output.frame)
        elif self.path == '/live.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                theTime = time.time()
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    # Original script logic: Throttle the stream to ~10fps
                    if time.time() - theTime >= 0.1:
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                        theTime = time.time()
            except Exception as e:
                print('Stopped: %s: %s', self.client_address, str(e))
        else:
            content = HTML.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Thread class to handle OpenCV camera capture separately from the HTTP Server
class CameraThread(threading.Thread):
    def __init__(self, output_buffer, width, height, device_index=0):
        super(CameraThread, self).__init__()
        self.output_buffer = output_buffer
        self.width = width
        self.height = height
        self.device_index = device_index
        self.running = True
        self.cap = cv2.VideoCapture(self.device_index)
        
        # Configure Camera
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        # Check if camera opened successfully
        if not self.cap.isOpened():
            raise RuntimeError("Couldn't talk to USB Camera")

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                # Encode the raw frame to JPEG
                # quality parameter 0-100 (higher is better quality but larger size)
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                _, jpeg = cv2.imencode('.jpg', frame, encode_param)
                
                # Write to the thread-safe buffer
                self.output_buffer.write(jpeg.tobytes())
            else:
                time.sleep(0.1) # Wait briefly if camera isn't ready

    def stop(self):
        self.running = False
        self.cap.release()

output = StreamingOutput()
camera_thread = CameraThread(output, streamWidth, streamHeight, cameraIndex)

try:
    print(f"Starting USB Camera Stream on port {portNum}...")
    camera_thread.start()
    
    address = ('', portNum)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    print("Stopping camera and server...")
    camera_thread.stop()
    camera_thread.join()
