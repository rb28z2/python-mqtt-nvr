#!/usr/bin/python
# -*- coding: utf-8 -*-
import config

import subprocess
import os
import ffmpy
import time
import paho.mqtt.client as mqtt
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import sys

scheduler = BackgroundScheduler(timezone=config.timeZone)
scheduler.start()

mqttUser = config.mqttUser
mqttPass = config.mqttPass


def stream1(camera, fileout, instance):
    global ffProcesses
    ffProcesses.append(ffmpy.FFmpeg(inputs={camera: '-y -hide_banner -loglevel panic'
                       },
                       outputs={fileout: '-c:v copy -c:a copy -f segment -strftime 1 -segment_time ' + str(config.segmentLength) + ' -segment_format mp4'
                       }))
    try:
        ffProcesses[instance].run()
    except ffmpy.FFRuntimeError, e:
        if e.exit_code and e.exit_code != 255:
            raise


def on_connect(
    client,
    userdata,
    flags,
    rc,
    ):
    print 'Connected with result code ' + str(rc)
    client.subscribe('cameras/nvr/record')


def on_message(client, userdata, msg):
    global instances
    global cameras
    global outfile
    print ('Instances: ', instances)
    print msg.topic + ' ' + str(msg.payload)
    if str(msg.payload) == 'record':
        print 'Record Received'
        client.publish('cameras/nvr', 'record')
        p = []
        for i in range(0, len(cameras)):
            p.append(threading.Thread(target=stream1, args=(cameras[i],
                     outfile[i], i)))
            instances = instances + 1
            print ('Starting recorder instance ', i)
            p[i].start()
    elif str(msg.payload) == 'stop':

        print 'Stop recieved'
        client.publish('cameras/nvr', 'stop')
        print 'Stopping job'
        if threading.activeCount() > 1:
            for i in range(threading.activeCount() - 1):
                try:
                    ffProcesses[i].process.terminate()
                except IndexError:
                    print 'Nothing to kill'
            instances = 1


def on_log(
    client,
    userdata,
    level,
    buf,
    ):
    print ('log: ', buf)


def garbageCollection():
    print '--- Running garbage collection ---'
    for (root, dirs, files) in os.walk(os.getcwd()):
        files = [fi for fi in files if fi.endswith('.mp4')]  # filter out stuff that isn't video files
        for name in files:
            toCheck = os.path.join(root, name)
            if os.stat(toCheck).st_mtime < time.time() - 7 * 86400:  # 7*86400 for 7 days
                os.remove(toCheck)


def main():

    global ffProcesses
    ffProcesses = []
    global instances
    instances = 1

    global cameras
    global outfile
    cameras = config.cameras
    outfile = config.outfile
    
    scheduler.add_job(garbageCollection, 'interval', hours=1)

    client = mqtt.Client(client_id='NVR-Client')
    if (config.mqttAuth):
        client.username_pw_set(mqttUser, password=mqttPass)
    client.on_connect = on_connect
    client.on_message = on_message

    # client.on_log = on_log

    client.connect(config.mqttIP, 1883)

    client.loop_start()

    print 'Started'
    while True:
        try:
            sleep(5)
        except KeyboardInterrupt:
            print '\nCONTROL-C - SHUTTING DOWN SCHEDULER'
            scheduler.shutdown()
            print 'SHUTTING DOWN MQTT CLIENT'
            client.loop_stop()
            print 'EXITING'
            sys.exit()


main()