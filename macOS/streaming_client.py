"""
Reference:
PiCamera documentation
https://picamera.readthedocs.org/en/release-1.10/recipes2.html

"""

import io
import socket
import struct
import time
import picamera


# Create socket and bind host
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('10.3.34.153', 8000))
connection = client.makefile('wb')

try:
    with picamera.PiCamera() as cam:
        cam.resolution = (320, 240)  # picamera resolution
        cam.framerate = 10  # 10 frames/sec
        time.sleep(2)  # Hold for 2 secs in order for camera to initialize
        start = time.time()
        stream = io.BytesIO()

        # Send jpg formatted video stream
        for _ in cam.capture_continuous(stream, 'jpeg', use_video_port=True):
            connection.write(struct.pack('<L', stream.tell().encode('utf-8')))
            connection.flush()
            stream.seek(0)
            connection.write((stream.read().decode('bytes')))
            if time.time() - start > 600:
                break
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L', 0))

finally:
    connection.close()
    client.close()
