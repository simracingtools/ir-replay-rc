from threading import Thread
import stomper
from websocket import create_connection
from websocket._exceptions import WebSocketConnectionClosedException

class RcServerConnector:
    rcServerUri = 'ws://192.168.178.154:8080/rcclient'
    frame = None
    irrc = None

    def __init__(self, statusFrame, irrc):
        self.frame = statusFrame
        self.irrc = irrc
        self.connected = False

    def connect(self, clientId):
        try:
            self.ws = create_connection(self.rcServerUri)
            self.receiver = ReceiveThread()
            self.receiver.start()

            self.ws.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")
            sub = stomper.subscribe("/user/rc/client-ack", clientId, ack='auto')
            self.ws.send(sub)
            sub = stomper.subscribe("/rc/" + str(clientId) + "/replayposition" , clientId, ack='auto')
            self.ws.send(sub)

            send_message = stomper.send("/app/rcclient", "Hello from " + str(clientId))
            self.ws.send(send_message)
        except Exception as e:
            print(str(e))

    def disconnect(self):
        if self.connected:
            self.ws.close()
            self.connected = False

class ReceiveThread(Thread):
    def __init__(self, connector):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.sentinel = True
        self.connector = connector

    def run(self):
        print("Receive thread started")
        while self.sentinel:
            try:
                d = self.ws.recv()
                if d:
                    m = MSG(d)
                    if m.type == 'CONNECTED':
                        self.frame.SetStatusText("RC server connected", 2)
                        self.connector.connected = True
                    else:
                        print("stomp message: " + str(m.message))
            except WebSocketConnectionClosedException:
                self.frame.SetStatusText("RC server disconnected", 2)
                self.connector.connected = False
                self.sentinel = False

        print("Receive thread terminated")

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

