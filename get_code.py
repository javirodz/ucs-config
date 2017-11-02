from ucsmsdk.ucshandle import UcsHandle
handle = UcsHandle("192.168.67.148","admin","password",secure=False)
handle.login()
#launch GUI
from ucsmsdk.utils.ucsguilaunch import ucs_gui_launch
ucs_gui_launch(handle)

#get ucs commands from the GUI
from ucsmsdk.utils.converttopython import convert_to_ucs_python
convert_to_ucs_python()
