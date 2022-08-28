# NetOver - Checking the overhead of networking

## Goal

* Check the overhead of networking for Image Processing based system.

## Co-goals 

* Check the overhead of python.
  
## Waypoints

* Writing a server and worker system. 
  * The server will choose random images (p x p pixels)
  * The worker will rotate them in 10 degrees y, times (using opencv's method) and calculate the sum
* The sum will be sent back to the server.
* The result of the experiment is the maximal fps for the calculation

### Points of Interest

* Multithreaded - same memory
* Multiprocess - shared memory
* Udp/Tcp loopback
* Udp/Tcp different computer

* x86_65
* Arm (raspberry pi3/4)
* Jetson

### Requirements

* Opencv for image processing, zmq for networking.

## Results

* Intel, single threaded, single core affinity : no difference between direct and tcp communication. 80 operations @ 30 fps.
* Same results within docker container.
* Rpi3, same characteristics : 8 / 7 operations, respectively.
  
### Raspberry pi 

Direct:
![rpi_direct](images/rpi_direct.png)

Localhost:
![localhost](images/rpi_socket.png)

### Intel i7 

Direct:
![intel_direct](images/intel_direct.png)

Localhost:
![socket](images/intel_socket.png)

## Running docker on rpi 

* Raw results of range(2,15,2) operations :
  
  * rpi docker direct
```
.{'0': [72.66088845930318, 38.369303404352735, 25.89687689829936, 19.590840801391344, 15.65623724161872, 13.104467952440272, 11.25902767509474]}
```

  * rpi direct
```
.{'0': [106.65942153154089, 56.825822645204845, 38.523460572164964, 29.040949571606646, 23.348802665007145, 19.524859689789505, 16.73763641271816]}
```

  * docker is slower by 150%. Maybe different accelerations of numpy ? 

