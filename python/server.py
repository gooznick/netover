
import numpy as np
import cv2
import time
import os
import config
import matplotlib.pyplot as plt
import zmq
import pickle


def send_to_client(socket, image, rotations):
    print("Sending")
    p = pickle.dumps((image, rotations))
    socket.send(p)
    return

def wait_for_client(socket):
    print("waiting")
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

  
    # from threading import Thread
    # import client
    # thread = Thread(target = client.main)
    # thread.start()
    # #thread.join()

    rotations_op =  [5, 10,15,20,25,30]
    options = {"0"}
    results = {}
    for affinity in options:
        fps = []
        for rotations in rotations_op:
            fps.append(server(500, rotations))
        results[str(affinity)] = fps

    for caption, fps in results.items():
        plt.plot(rotations_op, fps, label=caption)
        
    plt.xlabel('operations')
    plt.ylabel('fps')
    plt.grid(True)
    plt.legend()
    plt.title("500 x 500, 11th Gen Intel(R) Core(TM) i7-11800H @ 2.30GHz")
    plt.show()
    