
import numpy as np
import cv2
import time
import os
import config
import matplotlib
import matplotlib.pyplot as plt
import zmq
import pickle

import client

direct = False
rpi = True 

matplotlib.use('TkAgg')

def send_to_client(socket, image, rotations):
    print("Sending")
    if not direct:
        p = pickle.dumps((image, rotations))
        socket.send(p)
    else:
        client.work(image,rotations)

def wait_for_client(socket):
    print("waiting")
    if not direct:
        message = socket.recv()
    pass 

def server(pixels, rotations):
    image = np.random.randint(0,255,[pixels, pixels], dtype=np.uint8)
    context = zmq.Context()
    print ("Connecting to worker...")
    socket = context.socket(zmq.REQ)
    socket.connect(config.connect)
    print("connected")
    cycles = 0
    passed = 0.0
    while True:
        start = time.time()

        send_to_client(socket, image, rotations)
        response = wait_for_client(socket)

        cycles = cycles+1
        passed = passed + (time.time() - start)
        if passed > 1:
            fps = cycles/passed
            cycles = 0
            passed = 0
            break
    print(".", end="", flush=True)
    return fps

if __name__ == "__main__":

    # single core
    affinity_mask = {1}
    pid = 0
    os.sched_setaffinity(0, affinity_mask)

  
    rotations_op =  range(2,15,2) if rpi else range(20,150,20)
    options = {"0"}
    results = {}
    for affinity in options:
        fps = []
        for rotations in rotations_op:
            fps.append(server(config.pixels, rotations))
        results[str(affinity)] = fps

    for caption, fps in results.items():
        plt.plot(rotations_op, fps, label=caption)
        
    plt.xlabel('operations')
    plt.ylabel('fps')
    plt.grid(True)
    plt.legend()
    cpu = "Raspberry Pi 3B 1.2" if rpi else "Intel i7"
    plt.title(f"{config.pixels} x {config.pixels}, {'direct' if direct else config.bind},  {cpu}")
    plt.show()
    