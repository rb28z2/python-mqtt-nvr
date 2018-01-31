mqttIP = '192.168.3.2'
mqttAuth = False
mqttUser = 'username'
mqttPass = 'password'

timeZone = 'MST'

segmentLength = 300 #length of each segment in seconds

cameras = []
outfile = []
cameras.append('rtsp://admin:pass@192.168.1.17:554/cam/realmonitor?channel=1&subtype=0')
cameras.append('rtsp://admin:pass@192.168.1.16:554/cam/realmonitor?channel=1&subtype=0')
cameras.append('rtsp://admin:pass@192.168.1.15:554/cam/realmonitor?channel=1&subtype=0')
outfile.append('frontDoor//frontDoor-%Y-%m-%d_%H-%M-%S.mp4')
outfile.append('backyard//backyard-%Y-%m-%d_%H-%M-%S.mp4')
outfile.append('indoor//indoor-%Y-%m-%d_%H-%M-%S.mp4')