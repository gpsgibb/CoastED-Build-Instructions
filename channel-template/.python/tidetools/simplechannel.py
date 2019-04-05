
xmin_chan=1000.0
ymin=0.0
chanlen=5000.0
mindepth=5.0
maxchandepth=50.0
maxentrydepth=150.0
entry=1000.0
fanlen=1000.0

maxy=ymin+entry*2.0+fanlen*2.0+chanlen


def channelDepth( X ):
    y = X[1]

    narrowsy=ymin+entry+fanlen
    fany=ymin+entry

    if(y > narrowsy and y < narrowsy+chanlen):
        return(maxchandepth)
    elif(y<ymin+entry or y>narrowsy+chanlen+fanlen):
        return(maxentrydepth)


    ydist1=abs(fany-y);
    ydist2=abs(narrowsy+chanlen+fanlen-y)

    ydist=ydist1
    if(ydist1 > ydist2):
        ydist=ydist2

    scalef=ydist/fanlen
    depth = scalef*maxchandepth + (1.0-scalef)*maxentrydepth

    return depth

