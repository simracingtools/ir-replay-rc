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

__author__ = "Robert Bausdorf"
__contact__ = "rbausdorf@gmail.com"
__copyright__ = "2020, bausdorf engineering"
#__credits__ = ["One developer", "And another one", "etc"]
__date__ = "2019/06/01"
__deprecated__ = False
__email__ =  "rbausdorf@gmail.com"
__license__ = "GPLv3"
#__maintainer__ = "developer"
__status__ = "Beta"
__version__ = "1.0"

from irrcconfig import IrrcConfig
import wx
import time
import irRemoteControlRcFrame
import irsdk
from threading import Thread
from IrRemoteControl import IrRemoteControl
from rcserverconnect import RcServerConnector
from irrcconfig import IrrcConfig

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
                self.panel.SetStatusText('Sim disconnected', 0)
                rcServer.disconnect()

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

                    self.panel.SetStatusText('Sim connected', 0)
                    self.panel.playSpeed = ir['ReplayPlaySpeed']
                    self.panel.setSessionTime(ir['SessionTime'])
                    irRC.updateCamDict()

                    clientId = str(ir['DriverInfo']['DriverUserID'])
                    rcServer.connect(clientId)

            else:
                if(state.checkSessionChange(ir)):
                    self.panel.SetStatusText(state.getSessionName(), 1)

            time.sleep(1)
#            wx.CallAfter(self.panel.update)

        print('Thread finished!')
        rcServer.disconnect()

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
    config = IrrcConfig()
    rcServer = RcServerConnector(frame, irRC, config)
    
    frame.SetStatusText("Not connected", 0)
    frame.checker = ConnectionCheck(frame)
    frame.SetStatusText("RC server disconnected", 2)
    frame.checker.start()    
    frame.Show(True)     # Show the frame.


    app.MainLoop()