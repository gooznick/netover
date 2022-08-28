pixels = 300
rotate_times = 10

port = 5557



bind = f"ipc:///tmp/feeds/0"
connect = f"ipc:///tmp/feeds/0"

bind = f"tcp://*:{port}"
connect = f"tcp://10.42.0.170:{port}"

#bind = f"inproc://#1"
#connect = f"inproc://#1"


