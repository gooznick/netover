import cv2
import zmq
import time
import pickle 
import os
import numpy as np

import config

def work(image, rotations):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), 10, 1.0)
    for i in range(rotations):
        image = cv2.warpAffine(image, M, (w, h))
    print("Done")
def main():
    # single core
    affinity_mask = {1}
    pid = 0
    os.sched_setaffinity(0, affinity_mask)


    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(config.bind)
    while True:


        #  Wait for next request from client
        print("waiting for job")

        image, rotations = pickle.loads(socket.recv())
        work(image, rotations)

        socket.send(b"Done")

if __name__ == "__main__":
    main()