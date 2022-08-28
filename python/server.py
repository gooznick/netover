
import numpy as np
import cv2
import time
import os
import config
import matplotlib.pyplot as plt



def send_to_client(image, rotations):
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), 10, 1.0)
    for i in range(rotations):
        image = cv2.warpAffine(image, M, (w, h))
    return

def wait_for_client():
    pass 

def server(pixels, rotations):
    image = np.random.randint(0,255,[pixels, pixels], dtype=np.uint8)

    cycles = 0
    passed = 0.0
    while True:
        start = time.time()
        send_to_client(image, rotations)
        response = wait_for_client()
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
    affinity_mask = {0}
    pid = 0
    os.sched_setaffinity(0, affinity_mask)

  

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
    