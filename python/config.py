pixels = 300
rotate_times = 10

port = 5556
bind = f"ipc:///tmp/feeds/0"
connect = f"ipc:///tmp/feeds/0"


bind = f"tcp://*:{port}"
connect = f"tcp://localhost:{port}"


#bind = f"inproc://#1"
#connect = f"inproc://#1"


