import wx
import json
import time
import irRemoteControlRcFrame
import irsdk
from IrRemoteControl import IrRemoteControl
from threading import Thread
import stomper
from websocket import create_connection
from websocket._exceptions import WebSocketConnectionClosedException

class State:
    ir_connected = False
    sessionId = -1
    subSessionId = -1
    sessionNum = -1
    sessionState = -1

    def checkSessionChange(self, ir):
        sessionChange = False
        
        if self.sessionId != str(ir['WeekendInfo']['SessionID']):
            self.sessionId = str(ir['WeekendInfo']['SessionID'])
            sessionChange = True
                    
        if self.subSessionId != str(ir['WeekendInfo']['SubSessionID']):
            self.subSessionId = str(ir['WeekendInfo']['SubSessionID'])
            sessionChange = True

        if self.sessionNum != ir['SessionNum']:
            self.sessionNum = ir['SessionNum']
            sessionChange = True

        if self.sessionState != ir['SessionState']:
            self.sessionState = ir['SessionState']
            sessionChange = True

        if sessionChange:
            print('SessionId change: ' + self.getSessionName())

        return sessionChange

    def getSessionName(self):

        trackName = ir['WeekendInfo']['TrackName']
        return str(trackName) + '@' + str(self.sessionId) + '#' + str(self.subSessionId) + '#' + str(self.sessionNum)

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

class ReceiveThread(Thread):
    def __init__(self):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.sentinel = True
        self.ws = create_connection("ws://192.168.178.154:8080/rcclient")
        self.connected = False

    def run(self):
        while self.sentinel:
            try:
                d = self.ws.recv()
                if d:
                    m = MSG(d)
                    if m.type == 'CONNECTED':
                        frame.SetStatusText("RC server connected", 2)
                        self.connected = True
                    else:
                        print("stomp message: " + str(m.message))
            except WebSocketConnectionClosedException:
                frame.SetStatusText("RC server disconnected", 2)
                self.connected = False

#            if not self.connected:
#                self.ws = create_connection("ws://192.168.178.154:8080/rcclient")

class ConnectionCheck(Thread):
    
    def __init__(self, panel):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.panel = panel
        self.sentinel = True

    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        while self.sentinel:
            if state.ir_connected and not (ir.is_initialized and ir.is_connected):
                state.ir_connected = False
                # don't forget to reset all your in State variables
                state.sessionId = -1
                state.subSessionId = -1
                state.sessionNum = -1

                # we are shut down ir library (clear all internal variables)
                ir.shutdown()
                self.panel.SetStatusText('Not Connected', 0)

            elif not state.ir_connected:
                # Check if a dump file should be used to startup IRSDK
        #        if config.has_option('global', 'simulate'):
        #           is_startup = ir.startup(test_file=config['global']['simulate'])
        #            print('starting up using dump file: ' + str(config['global']['simulate']))
        #        else:
                is_startup = ir.startup()

                if is_startup and ir.is_initialized and ir.is_connected:
                    state.ir_connected = True
                    state.checkSessionChange(ir)
                    self.panel.SetStatusText(state.getSessionName(), 1)

                    self.panel.SetStatusText('Connected', 0)
                    self.panel.playSpeed = ir['ReplayPlaySpeed']
                    self.panel.setSessionTime(ir['SessionTime'])
                    irRC.updateCamDict()

                    clientId = str(ir['DriverInfo']['DriverUserID'])
                    receiver.ws.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")
                    sub = stomper.subscribe("/user/rc/client-ack", clientId, ack='auto')
                    receiver.ws.send(sub)
                    sub = stomper.subscribe("/rc/" + str(clientId) + "/replayposition" , clientId, ack='auto')
                    receiver.ws.send(sub)

                    send_message = stomper.send("/app/rcclient", "Hello from " + str(clientId))
                    receiver.ws.send(send_message)

            else:
                if(state.checkSessionChange(ir)):
                    self.panel.SetStatusText(state.getSessionName(), 1)

            time.sleep(1)
#            wx.CallAfter(self.panel.update)

        print('Thread finished!')
        receiver.ws.close()

def iRSessionTimeToWxDateTime(sessionTime):
    hours = int(sessionTime / 3600)
    minutes = int((sessionTime - (hours * 3600)) / 60)
    seconds = int(sessionTime - (hours * 3600) - (minutes * 60))
    print(str(hours) + ':' + str(minutes) + ':' + str(seconds))
    return wx.DateTime.FromHMS(hours, minutes, seconds)

if __name__ == '__main__':
    ir = irsdk.IRSDK()
    state = State()
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    irRC = IrRemoteControl(ir)
    frame = irRemoteControlRcFrame.irRemoteControlRcFrame(None, irRC) # A Frame is a top-level window.

    receiver = ReceiveThread()
    receiver.start()
    
    frame.SetStatusText("Not connected", 0)
    frame.checker = ConnectionCheck(frame)
    frame.SetStatusText("RC server disconnected", 2)
    frame.checker.start()    
    frame.Show(True)     # Show the frame.


    app.MainLoop()