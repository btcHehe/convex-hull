import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# define world size
WorldxSize = 20
WorldySize = 20

# minimal length of triangle side
minA = 0.5
# maximum step of point
maxStep = 0.5
# number of frames of animation per second
FPS = 30


class tiger:
    def __init__(self, px, py, a):
        self.px = px
        self.py = py
        self.a = a  # length of the side of triangle
        self.vertx = []
        self.verty = []

    def genVertex(self):
        R = self.a * np.sqrt(3) / 3
        randAlpha = random.uniform(0, 2 * np.pi)  # random point from the circle with radius R
        V1x = R * np.sin(randAlpha) + self.px
        V1y = R * np.cos(randAlpha) + self.py
        a = (V1y - self.py) / (V1x - self.px)  # straight line coeffcients
        b = self.py - a * self.px
        r = self.a * np.sqrt(3) / 6
        self.vertx = [self.px, self.px + self.a / 2, self.px - self.a / 2, self.px]
        self.verty = [self.py + R, self.py - r, self.py - r, self.py + R]


def genTigers(tigNum):
    tmpTigersArr = []
    for i in range(tigNum):
        tigerOntiger = True
        randx = 0
        randy = 0
        randA = 2
        while tigerOntiger:
            randx = random.uniform(0, WorldxSize)
            randy = random.uniform(0, WorldySize)
            randA = random.uniform(minA, 2)
            points = 0
            for tigers in tmpTigersArr:  # so every random point has different position
                if np.abs(randx - tigers.px) > 0.1 and np.abs(randy - tigers.py) > 0.1:
                    points += 1
            if points == len(tmpTigersArr):
                break

        tmpTiger = tiger(randx, randy, randA)
        tmpTiger.genVertex()
        tmpTigersArr.append(tmpTiger)
    return tmpTigersArr


def jarvis(tigArray):
    TmptigArr = tigArray.copy()
    tigArr = []
    for i, k in enumerate(tigArray):
        for j in range(len(k.vertx) - 1):
            tmpTiger = tiger(k.vertx[j], k.verty[j], 0)
            tigArr.append(tmpTiger)

    ycrd = []
    # finding Q1 and P1 points
    for tgr in tigArr:
        ycrd.append(tgr.py)

    minyIndex = np.argmin(np.array(ycrd))
    maxyIndex = np.argmax(np.array(ycrd))
    tigArrR = tigArr.copy()
    tigArrL = tigArr.copy()

    tigP1 = tigArr[minyIndex]
    tigQ1 = tigArr[maxyIndex]

    rightPoints = []
    leftPoints = []

    # right chain ordering
    lastTig = tigP1
    rightPoints.append(lastTig)
    vecR = np.array([1, 0])
    vecL = np.array([-1, 0])

    # right side chain
    while lastTig.py != tigQ1.py and lastTig.px != tigQ1.px:
        xc = []
        yc = []
        alpha = []
        for i in tigArrR:
            xc.append(i.px)
            yc.append(i.py)
        for j in range(len(xc)):
            if xc[j] == lastTig.px:
                alpha.append(2 * np.pi)
                continue
            ay = yc[j] - lastTig.py
            ax = xc[j] - lastTig.px
            vecN = np.array([ax, ay])
            normVecN = vecN / (np.sqrt(vecN[0] ** 2 + vecN[1] ** 2))
            angle = np.arctan2(normVecN[1], normVecN[0]) - np.arctan2(vecR[1], vecR[0])
            if angle < 0:
                angle = angle + 2 * np.pi
            alpha.append(angle * 360 / (2 * np.pi))

        minAngleIndex = np.argmin(alpha)
        lastTig = tigArrR.pop(minAngleIndex)
        rightPoints.append(lastTig)

    leftPoints.append(lastTig)

    # left side chain
    while lastTig.py != tigP1.py and lastTig.px != tigP1.px:
        xc = []
        yc = []
        alpha = []
        for i in tigArrL:
            xc.append(i.px)
            yc.append(i.py)
        for j in range(len(xc)):
            if xc[j] == lastTig.px:
                alpha.append(2 * np.pi)
                continue
            ay = yc[j] - lastTig.py
            ax = xc[j] - lastTig.px
            vecN = np.array([ax, ay])
            normVecN = vecN / (np.sqrt(vecN[0] ** 2 + vecN[1] ** 2))
            angle = np.arctan2(normVecN[1], normVecN[0]) - np.arctan2(vecL[1], vecL[0])
            alpha.append(angle * 360 / (2 * np.pi))

        minAngleIndex = np.argmin(alpha)
        lastTig = tigArrL.pop(minAngleIndex)
        leftPoints.append(lastTig)

    return rightPoints, leftPoints


def moveTigers(tList):
    for ti in tList:
        rndx = random.uniform(0, maxStep)
        rndy = random.uniform(0, maxStep)
        rndSGNx = random.choice([True, False])
        rndSGNy = random.choice([True, False])
        if rndSGNx:
            ti.px += rndx
        else:
            ti.px -= rndx
        if rndSGNy:
            ti.py += rndy
        else:
            ti.py -= rndy
        ti.genVertex()
    return tList


# drawing everything
def makePlot(rpts, lpts, tArr):
    xr = []
    yr = []
    xl = []
    yl = []

    for pt in rpts:
        xr.append(pt.px)
        yr.append(pt.py)

    for pt in lpts:
        xl.append(pt.px)
        yl.append(pt.py)

    xcoords = []
    ycoords = []

    # drawing triangles
    for t in tArr:
        xw = t.vertx
        yw = t.verty
        xcoords.append(t.px)
        ycoords.append(t.py)
        plt.plot(xw, yw)

    # drawing points and convex
    plt.scatter(xcoords, ycoords)
    plt.plot(xr, yr)
    plt.plot(xl, yl)


# updating drawn frames
def update(i):
    global tigersArr
    plt.clf()
    rchain, lchain = jarvis(tigersArr)
    plt.title(f'Frame number: {i}')
    makePlot(rchain, lchain, tigersArr.copy())
    tigersArr = moveTigers(tigersArr)

if __name__ == '__main__' :
    tigersArr = genTigers(20)
    fig, ax = plt.subplots()
    animation = FuncAnimation(fig, update, interval=1000/FPS)
    plt.show()
