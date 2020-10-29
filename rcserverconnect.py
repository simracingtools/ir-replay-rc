# Copyright (C) 2020 rbaus
# 
# This file is part of ir-replay-rc.
# 
# ir-replay-rc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ir-replay-rc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ir-replay-rc.  If not, see <http://www.gnu.org/licenses/>.


import sys
import json
import time
from os import system
from threading import Thread
import stomper
from websocket import create_connection
from websocket._exceptions import WebSocketConnectionClosedException

class RcServerConnector:
    rcServerUri = 'ws://192.168.178.154:8080/rcclient'
    frame = None
    irrc = None

    def __init__(self, statusFrame, irrc, config):
        self.frame = statusFrame
        self.irrc = irrc
        self.rcServerUri = config.getWsUrl()
        self.connected = False

    def connect(self, clientId):
        try:
            self.ws = create_connection(self.rcServerUri)
            self.receiver = ReceiveThread(self)
            self.receiver.start()
            
            self.ws.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")
            sub = stomper.subscribe("/user/rc/client-ack", clientId, ack='auto')
            self.ws.send(sub)
            sub = stomper.subscribe("/rc/" + str(clientId) + "/replayposition" , clientId, ack='auto')
            self.ws.send(sub)

            send_message = stomper.send("/app/rcclient", str(clientId))
            self.ws.send(send_message)

            self.heartbeat = HeartbeatThread(self, clientId)
            self.heartbeat.start()
        except Exception as e:
            self.frame.SetStatusText(self.rcServerUri + ': ' + str(e), 2)
            #print(str(e))

    def disconnect(self):
        if self.connected:
            self.ws.close()
            self.connected = False

class ReceiveThread(Thread):
    def __init__(self, connector):
        """Init receiver Thread Class."""
        Thread.__init__(self)
        self.sentinel = True
        self.connector = connector

    def run(self):
        print("Receive thread started")
        while self.sentinel:
            try:
                d = self.connector.ws.recv()
                if d:
                    m = MSG(d)
                    if m.type == 'CONNECTED':
                        self.connector.frame.SetStatusText(self.connector.rcServerUri + " connected", 2)
                        self.connector.connected = True
                    else:
                        print("stomp message: " + str(m.message))
                        try:
                            message = json.loads(str(m.message))
                            if message['messageType'] == 'replayTime':
                                self.connector.irrc.setTimePosition(message['timestamp'], message['driverId'])
                                self.connector.frame.setSessionTime(message['timestamp'] / 1000)
                        except json.decoder.JSONDecodeError as jserr:
                            print(str(jserr))

            except WebSocketConnectionClosedException:
                try:
                    self.connector.frame.SetStatusText(self.connector.rcServerUri + " disconnected", 2)
                    self.connector.connected = False
                    self.sentinel = False
                except RuntimeError as e:
                    print(str(e))
                    sys.exit(0)


        print("Receive thread terminated")

class HeartbeatThread(Thread):
    def __init__(self, connector, clientId):
        """Init heartbeat Thread Class."""
        Thread.__init__(self)
        self.sentinel = True
        self.connector = connector
        self.clientId = clientId

    def run(self):
        print("Receive thread started")
        while self.sentinel:
            try:
                time.sleep(10)
                send_message = stomper.send("/app/rcclient", str(self.clientId))
                self.connector.ws.send(send_message)
            except WebSocketConnectionClosedException:
                self.sentinel = False

class MSG(object):
    def __init__(self, msg):
        self.msg = msg
        sp = self.msg.split("\n")
        self.type = sp[0]
        self.destination = sp[1].split(":")[1]
        self.content = sp[2].split(":")[1]
        if self.type == 'MESSAGE':
            self.subs = sp[3].split(":")[1]
            self.id = sp[4].split(":")[1]
            self.len = sp[5].split(":")[1]
            # sp[6] is just a \n
            self.message = ''.join(sp[7:])[0:-1]  # take the last part of the message minus the last character which is \00

