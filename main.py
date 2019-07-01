from navigation.rc import RCLib
import time
import navigation.imu as imu


rc = RCLib()

rc.setmode('MANUAL')

rc.arm()

rc.forward("time", 6, 0.25)
rc.yaw("time", 1.2, -0.25)
rc.forward("time", 3, 0.25)
rc.yaw("time", 1.2, -0.25)
rc.forward("time", 6, 0.25)
