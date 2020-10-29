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


import wx
import RcCode
import IrRemoteControl

# Implementing RcFrame
class irRemoteControlRcFrame( RcCode.RcFrame ):
	playSpeed = 0
	checker = None

	def __init__( self, parent, irRemote ):
		RcCode.RcFrame.__init__( self, parent )
		self.SetStatusWidths([100, 250, -1])
		self.irrc = irRemote

	def setSessionTime(self, sessionTimeSeconds):
		print("set session time: " + str(sessionTimeSeconds))

		hours = int(sessionTimeSeconds / 3600)
		minutes = int((sessionTimeSeconds - (hours * 3600)) / 60)
		seconds = int(sessionTimeSeconds - (hours * 3600) - (minutes * 60))

		self.session_time_pick.SetTime(hours, minutes, seconds)
	

	# Handlers for RcFrame events.
	def handle_keypress( self, event ):
		print("Key: " + str(event.GetKeyCode()))
		pass

	def frLeftDown( self, event ):
		if self.playSpeed >= 0:
			self.playSpeed = -2
		elif self.playSpeed < 0:
			self.playSpeed *= 2

		self.irrc.updatePlaySpeed(self.playSpeed, False)
		event.Skip()

	def lfLeftDown( self, event ):
		self.irrc.updateShownFrame(-2)
		event.Skip()

	def ppLeftDown( self, event ):
		if self.playSpeed == 0:
			self.playSpeed = 1
		else:
			self.playSpeed = 0

		self.irrc.updatePlaySpeed(self.playSpeed, False)
		event.Skip()

	def nfLeftDown( self, event ):
		self.irrc.updateShownFrame(2)
		event.Skip()

	def ffLeftDown( self, event ):
		if self.playSpeed <= 0:
			self.playSpeed = 2
		elif self.playSpeed > 0:
			self.playSpeed *= 2

		self.irrc.updatePlaySpeed(self.playSpeed, False)
		event.Skip()

	def liveLeftDown( self, event ):
		self.irrc.toLivePosition()
		event.Skip()

	def camCase( self, event ):
		self.irrc.camSwitch('Chase')
		event.Skip()

	def camFarChase( self, event ):
		self.irrc.camSwitch('Far Chase')
		event.Skip()

	def camRearChase( self, event ):
		self.irrc.camSwitch('Rear Chase')
		event.Skip()

	def camCockpit( self, event ):
		self.irrc.camSwitch('Cockpit')
		event.Skip()

	def setTimePosition( self, event ):
		irSessionTime = event.GetDate().GetHour() * 3600
		irSessionTime += event.GetDate().GetMinute() * 60
		irSessionTime += event.GetDate().GetSecond()
		self.irrc.setTimePosition(irSessionTime * 1000)
		event.Skip()

	def closeWindow( self, event ):
		self.checker.sentinel = False
		event.Skip()

