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

    def update_play_speed(self, play_speed, slow):
        if self.ir.is_initialized and self.ir.is_connected:
            self.ir.replay_set_play_speed(play_speed, slow)

    def update_shown_frame(self, frame_delta):
        current_frame = self.ir['ReplayFrameNum']
        if self.ir.is_initialized and self.ir.is_connected and current_frame > 0:
            self.ir.replay_set_play_position(RpyPosMode.current, frame_delta)

    def to_live_position(self):
        if self.ir.is_initialized and self.ir.is_connected:
            self.ir.replay_set_play_position(RpyPosMode.end, 0)
            self.ir.replay_set_play_speed(1, False)


    def cam_switch(self, cam_name):
        if self.ir.is_initialized and self.ir.is_connected:
            cam_car_idx = self.ir['CamCarIdx']
            cam_car_no = self.ir['DriverInfo']['Drivers'][cam_car_idx]['CarNumberRaw']
            if self.cams[cam_name]:
                self.ir.cam_switch_num(cam_car_no, self.cams[cam_name]['GroupNum'], 1)
                #cam_switch_pos(self, position=0, group=1, camera=0)
            else:
                print('Cam group not found')

    def set_time_position(self, session_time, team_id=-1):
        if self.ir.is_initialized and self.ir.is_connected:
            cam_car_no = -1
            print("set time on driver " + str(team_id) + " to " + str(session_time))
            if team_id > 0:
                for driver in self.ir['DriverInfo']['Drivers']:
                    if driver['TeamID'] == team_id:
                        cam_car_no = driver['CarNumberRaw']
                        print("found driver " + str(driver['UserID']) + ", carNo: " + str(cam_car_no))
                        break
                if cam_car_no == -1:
                    for driver in self.ir['DriverInfo']['Drivers']:
                        if driver['UserID'] == team_id:
                            cam_car_no = driver['CarNumberRaw']
                            print("found driver " + str(driver['UserID']) + ", carNo: " + str(cam_car_no))
                            break

            cam_group_number = self.ir['CamGroupNumber']
            if self.ir['CameraInfo']['Groups'][cam_group_number]['GroupName'] not in \
                    ['Chase', 'Far Chase', 'Rear Chase', 'Cockpit']:
                cam_group_number = self.cams['Chase']['GroupNum']

            self.ir.replay_search_session_time(self.ir['SessionNum'], session_time)
            if cam_car_no > -1:
                self.ir.cam_switch_num(cam_car_no, cam_group_number, 1)

    def update_cam_dict(self):
        if self.ir.is_initialized and self.ir.is_connected:
            for cam_group in self.ir['CameraInfo']['Groups']:
                self.cams[cam_group['GroupName']] = cam_group

