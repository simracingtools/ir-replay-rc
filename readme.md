# iRacing Replay Remote Control

This app is able to control an iRacing replay. It is also able to connect to a race control server unsing a websocket and receive replay positions (timestamps) from the server.

For server information see 
https://github.com/simracingtools/racecontrol-server

To build:

    pyinstaller --clean --noconsole -F .\irRcApp.py

     & 'C:\Program Files (x86)\Inno Setup 6\ISCC.exe' .\irrcapp.iss
