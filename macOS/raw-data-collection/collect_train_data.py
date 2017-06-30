"""
References:
https://docs.python.org/2.7/howto/sockets.html
https://www.pygame.org/docs/ref/key.html - * pygame/GoPiGo Keys interpret

Zheng Wang
https://github.com/hamuchiwa/AutoRCCar/blob/master/
computer/collect_training_data.py

"""

import cv2
import pygame
import serial
import socket
import numpy as np


class CollectData(object):

    def __init__(self):

        self.server_socket = socket.socket()
        self.server_socket.bind(('10.3.34.153', 8000))
        self.server_socket.listen(0)

        # Accept just a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # Connect to a serial port
        self.ser = serial.Serial('/dev/tty.Bluetooth-Incoming-Port', 115200, timeout=1)
        self.send_inst = True

        # Create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')

        pygame.init()
        self.collect_image()

    def collect_image(self):

        saved_frame = 0
        total_frame = 0

        # Initialize image collection
        print 'Start collecting images...'
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 4), 'float')

        # Stream video frames one-by-one
        try:
            stream_bytes = ' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)
                    # Parse/Select lower half of the image
                    roi = img[120:240, :]
                    # Save streamed images
                    cv2.imwrite('~/self-driving-car/macOS/training_img/frame{:>05}.jpg'.format(frame), img)
                    cv2.imshow('roi_image', roi)
                    cv2.imshow('img', img)

                    # Reshape the ROI image into one row array
                    tmp_array = roi.reshape(1, 38400).astype(np.float32)
                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()
                            # simple orders
                            if key_input[pygame.K_w]:
                                print "Forward"
                                saved_frame += 1
                                image_array = np.vstack((image_array, tmp_array))
                                label_array = np.vstack((label_array, self.k[2]))
                                self.ser.write(chr(1))
                            elif key_input[pygame.K_s]:
                                print "Reverse"
                                saved_frame += 1
                                image_array = np.vstack((image_array, tmp_array))
                                label_array = np.vstack((label_array, self.k[3]))
                                self.ser.write(chr(2))
                            elif key_input[pygame.K_d]:
                                print "Right"
                                image_array = np.vstack((image_array, tmp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                self.ser.write(chr(3))
                            elif key_input[pygame.K_a]:
                                print "Left"
                                image_array = np.vstack((image_array, tmp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                self.ser.write(chr(4))
                            elif key_input[pygame.K_x]:
                                print "Stop"
                                image_array = np.vstack((image_array, tmp_array))
                                label_array = np.vstack((label_array, self.k[4]))
                                saved_frame += 1
                                self.ser.write(chr(5))
                            elif key_input[pygame.K_z]:
                                print 'Exit'
                                self.send_inst = False
                                self.ser.write(chr(0))
                                break
                        elif event.type == pygame.KEYUP:
                            self.ser.write(chr(0))

            # Save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]

            # Save training data as a numpy file (.npz format)
            np.savez('~/self-driving-car/macOS/training_data_temp/test08.npz', train=train, train_labels=train_labels)
            e2 = cv2.getTickCount()

            # Calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print('Streaming duration:', time0)

            print(train.shape)
            print(train_labels.shape)
            print('Total frame:', total_frame)
            print('Saved frame:', saved_frame)
            print('Dropped frame', total_frame - saved_frame)

        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    CollectData()
