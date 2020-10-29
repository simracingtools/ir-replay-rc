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

import irsdk
from irsdk import RpyPosMode

class IrRemoteControl:
    ir = None
    cams = {}

    def __init__( self, ir ):
        self.ir = ir

    def updatePlaySpeed(self, playSpeed, slow):
        if self.ir.is_initialized and self.ir.is_connected:
            self.ir.replay_set_play_speed(playSpeed, slow)

    def updateShownFrame(self, frameDelta):
        currentFrame = self.ir['ReplayFrameNum']
        if self.ir.is_initialized and self.ir.is_connected and currentFrame > 0:
            self.ir.replay_set_play_position(RpyPosMode.current, frameDelta)

    def toLivePosition(self):
        if self.ir.is_initialized and self.ir.is_connected:
            self.ir.replay_set_play_position(RpyPosMode.end, 0)

    def camSwitch(self, camName):
        if self.ir.is_initialized and self.ir.is_connected:
            camCarIdx = self.ir['CamCarIdx']
            camCarNo = self.ir['DriverInfo']['Drivers'][camCarIdx]['CarNumberRaw']
            if self.cams[camName]:
                self.ir.cam_switch_num(camCarNo, self.cams[camName]['GroupNum'], 1)
                #cam_switch_pos(self, position=0, group=1, camera=0)
            else:
                print('Cam group not found')

    def setTimePosition(self, sessionTime, teamId=-1):
        if self.ir.is_initialized and self.ir.is_connected:
            camCarNo = -1
            print("set time on driver " + str(teamId) + " to " + str(sessionTime))
            if teamId > 0:
                for driver in self.ir['DriverInfo']['Drivers']:
                    if driver['TeamID'] == teamId:
                        camCarNo = driver['CarNumberRaw']
                        print("found driver " + str(driver['UserID']) + ", carNo: " + str(camCarNo))
                        break

            camGroupNumber = self.ir['CamGroupNumber']
            if not camGroupNumber in [9, 20, 21, 22]:
                camGroupNumber = 20 # Chase

            self.ir.replay_search_session_time(self.ir['SessionNum'], sessionTime)
            if camCarNo > -1:
                self.ir.cam_switch_num(camCarNo, camGroupNumber, 1)

    def updateCamDict(self):
        if self.ir.is_initialized and self.ir.is_connected:
            for camGroup in self.ir['CameraInfo']['Groups']:
                self.cams[camGroup['GroupName']] = camGroup

