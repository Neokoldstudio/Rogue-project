import math

#all "physics" functions, relatives to the movements
def Lerp(spd, wantedSpeed):
    return(spd * 0.8 + wantedSpeed*0.2)

def lenght(v):
    return (math.sqrt(v[0]*v[0] + v[1]*v[1]))

# def DistBox(p,center, size):
#     dx = max(abs(p[0] - center[0]) - size / 2, 0)
#     dy = max(abs(p[1] - center[1]) - size / 2, 0)

#     distPoint = (dx,dy)
#     return lenght(distPoint)

def DistCircleToCircle(p1, p2, radius1, radius2):
    distTpl = (p2[0]-p1[0], p2[1]-p1[1])
    return(lenght(distTpl)-(radius1+radius2))

def DistBoxToCircle(p, center, size, radius):
    dx = max(abs(p[0] - center[0]) - size[0] / 2, 0)
    dy = max(abs(p[1] - center[1]) - size[1] / 2, 0)

    distPoint = (dx,dy)
    return lenght(distPoint) - radius