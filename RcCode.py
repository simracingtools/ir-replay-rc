# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv

###########################################################################
## Class RcFrame
###########################################################################

class RcFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"iRacing Remote Control", pos = wx.DefaultPosition, size = wx.Size( 750,165 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 750,165 ), wx.DefaultSize )

		g_sizer_1 = wx.GridSizer( 3, 6, 5, 5 )

		self.fr_button = wx.Button( self, wx.ID_ANY, u"FR", wx.DefaultPosition, wx.DefaultSize, 0 )
		g_sizer_1.Add( self.fr_button, 0, wx.ALL, 5 )

		self.lf_button = wx.Button( self, wx.ID_ANY, u"Last frame", wx.DefaultPosition, wx.DefaultSize, 0 )
		g_sizer_1.Add( self.lf_button, 0, wx.ALL, 5 )

		self.play_button = wx.Button( self, wx.ID_ANY, u"Play/Pause", wx.DefaultPosition, wx.DefaultSize, 0 )
		g_sizer_1.Add( self.play_button, 0, wx.ALL, 5 )

		self.nf_button = wx.Button( self, wx.ID_ANY, u"Next frame", wx.DefaultPosition, wx.DefaultSize, 0 )
		g_sizer_1.Add( self.nf_button, 0, wx.ALL, 5 )

		self.ff_button = wx.Button( self, wx.ID_ANY, u"FF", wx.DefaultPosition, wx.DefaultSize, 0 )
		g_sizer_1.Add( self.ff_button, 0, wx.ALL, 5 )

		self.live_button = wx.Button( self, wx.ID_ANY, u"Live", wx.DefaultPosition, wx.DefaultSize, 0 )
		g_sizer_1.Add( self.live_button, 0, wx.ALL, 5 )

		self.ui_button = wx.Button( self, wx.ID_ANY, u"Hide/Show UI", wx.DefaultPosition, wx.DefaultSize, 0 )
		g_sizer_1.Add( self.ui_button, 0, wx.ALL, 5 )

		self.case_btn = wx.Button( self, wx.ID_ANY, u"Chase", wx.DefaultPosition, wx.DefaultSize, 0 )
		g_sizer_1.Add( self.case_btn, 0, wx.ALL, 5 )

		self.far_chase_btn = wx.Button( self, wx.ID_ANY, u"Far chase", wx.DefaultPosition, wx.DefaultSize, 0 )
		g_sizer_1.Add( self.far_chase_btn, 0, wx.ALL, 5 )

		self.rear_chase_btn = wx.Button( self, wx.ID_ANY, u"Rear chase", wx.DefaultPosition, wx.DefaultSize, 0 )
		g_sizer_1.Add( self.rear_chase_btn, 0, wx.ALL, 5 )

		self.cockpit_btn = wx.Button( self, wx.ID_ANY, u"Cockpit", wx.DefaultPosition, wx.DefaultSize, 0 )
		g_sizer_1.Add( self.cockpit_btn, 0, wx.ALL, 5 )

		self.session_time_pick = wx.adv.TimePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.TP_DEFAULT )
		g_sizer_1.Add( self.session_time_pick, 0, wx.ALL, 5 )


		self.SetSizer( g_sizer_1 )
		self.Layout()
		self.staturBar = self.CreateStatusBar( 3, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CHAR_HOOK, self.handle_keypress )
		self.Bind( wx.EVT_CLOSE, self.closeWindow )
		self.fr_button.Bind( wx.EVT_LEFT_DOWN, self.frLeftDown )
		self.lf_button.Bind( wx.EVT_LEFT_DOWN, self.lfLeftDown )
		self.play_button.Bind( wx.EVT_LEFT_DOWN, self.ppLeftDown )
		self.nf_button.Bind( wx.EVT_LEFT_DOWN, self.nfLeftDown )
		self.ff_button.Bind( wx.EVT_LEFT_DOWN, self.ffLeftDown )
		self.live_button.Bind( wx.EVT_LEFT_DOWN, self.liveLeftDown )
		self.case_btn.Bind( wx.EVT_LEFT_DOWN, self.camCase )
		self.far_chase_btn.Bind( wx.EVT_LEFT_DOWN, self.camFarChase )
		self.rear_chase_btn.Bind( wx.EVT_LEFT_DOWN, self.camRearChase )
		self.cockpit_btn.Bind( wx.EVT_LEFT_DOWN, self.camCockpit )
		self.session_time_pick.Bind( wx.adv.EVT_TIME_CHANGED, self.setTimePosition )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def handle_keypress( self, event ):
		event.Skip()

	def closeWindow( self, event ):
		event.Skip()

	def frLeftDown( self, event ):
		event.Skip()

	def lfLeftDown( self, event ):
		event.Skip()

	def ppLeftDown( self, event ):
		event.Skip()

	def nfLeftDown( self, event ):
		event.Skip()

	def ffLeftDown( self, event ):
		event.Skip()

	def liveLeftDown( self, event ):
		event.Skip()

	def camCase( self, event ):
		event.Skip()

	def camFarChase( self, event ):
		event.Skip()

	def camRearChase( self, event ):
		event.Skip()

	def camCockpit( self, event ):
		event.Skip()

	def setTimePosition( self, event ):
		event.Skip()


