# Only works for new turbines.dat format
import os


class Wind():
    def __init__(self, direction, speed, u0_height, featureheight, relaxtime):
        self.direction = direction
        self.speed = speed
        self.u0_height = u0_height
        self.featureheight = featureheight
        self.relaxtime = relaxtime


def readWind():
    filename = "wind.dat"
    
    fileExists = os.path.exists(filename)
    if not (fileExists):
        exit( "Wind file '" + filename + "' does not exist")
        
    windfile = open ("wind.dat", "r")
    words = windfile.readline().split()
    windfile.close()

    if ( len(words) < 4 ):
        exitMessage="wind.dat must contain:\n" + \
            "wind_direction wind_speed wind_height feature_height <relax_time optional>\n"

        exit(exitMessage)
        
    winddir = float( words[0] )
    windspeed = float( words[1] )
    u0_height = float( words[2] )
    featureheight = float( words[3] )

    if(len(words)<5):
        relaxtime = 0.0
    else:
        relaxtime = float( words[4] )

    if(abs(relaxtime) > 0.000001):
        print "*** WARNING: non-zero relaxtime does not work with SEM BCs"

    return Wind(winddir, windspeed, u0_height, featureheight, relaxtime)
