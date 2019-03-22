import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import multiprocessing as mp
import os
import time
from matplotlib.widgets import Cursor
from scipy import stats as scpStats
import numpy as np
# import matplotlib

import threading
from queue import Queue
import cv2

# matplotlib.interactive(True)


class dataProcess(threading.Thread):


    def __init__(self, threadID, name):

        threading.Thread.__init__(self)

        self.threadID = threadID
        self.name = name

    def run(self):
        global clickCoordinate
        global clickRegistered
        global exitFlag
        global drawCallPending
        global drawCallQueue
        global xAxis
        global yAxis
        global data

        print ("Starting " + self.name)
        self.defineXaxis()
        # print(xAxis)
        xAxis = np.array(xAxis)
        xAxis = xAxis[xAxis[:,0].argsort()]
        # xAxis = np.sort(xAxis, axis=0)
        # print(xAxis)

        slope, intercept, r_value, p_value, std_err = scpStats.linregress(xAxis[:,0].flatten(), xAxis[:,1].flatten())
        line = slope*xAxis[:,0].flatten()+intercept
        drawCallQueue.put(["plt.plot(xAxis[:,0].flatten(), line, 'r-', xAxis[:,0].flatten(),xAxis[:,1].flatten(),'o')",line])
        drawCallPending = True

        self.defineYaxis()

        yAxis = np.array(yAxis)
        yAxis = yAxis[yAxis[:,0].argsort()]

        slope, intercept, r_value, p_value, std_err = scpStats.linregress(yAxis[:,0].flatten(), yAxis[:,1].flatten())
        line = slope*yAxis[:,0].flatten()+intercept
        drawCallQueue.put(["plt.plot(yAxis[:,0].flatten(), line, 'r-', yAxis[:,0].flatten(),yAxis[:,1].flatten(),'o')",line])
        drawCallPending = True

        self.getDataPoints()

        data = np.array(data)
        drawCallQueue.put(["plt.plot(data[:,0].flatten(), data[:,1].flatten(),'+')","-"])
        drawCallPending = True

        # exitFlag = True

        print ("Exiting " + self.name)

    def defineYaxis(self):
        global clickCoordinate
        global clickRegistered
        global exitFlag
        global yAxis

        print("Pick points on Y axis...")
        choice = "y"
        while choice != 'n':
            if clickRegistered:
                value = input('What is the Y value? : ')
                yAxis.append([clickCoordinate[0],clickCoordinate[1],float(value)])
                clickRegistered = False
                choice = input("More axis points available? (y/n)")
            time.sleep(0.5)

        print(yAxis)

    def defineXaxis(self):
        global clickCoordinate
        global clickRegistered
        global exitFlag
        global xAxis

        print("Pick points on X axis...")
        choice = 'y'
        while choice != 'n':
            # print()
            if clickRegistered:
                value = input('What is the X value? : ')
                xAxis.append([clickCoordinate[0],clickCoordinate[1], float(value)])
                clickRegistered = False
                choice = input("More axis points available? (y/n)")
            time.sleep(0.5)
        print(xAxis)

    def getDataPoints(self):
        global data
        global clickCoordinate
        global clickRegistered
        global exitFlag
        print("Pick points on the curve...")

        choice = "y"
        while choice != "n":
            if clickRegistered:
                data.append(clickCoordinate)
                clickRegistered = False
                choice = input("More data available? (y/n)")


# def getData(clickRegistered,clickCoordinate):
#     defineXaxis(clickRegistered,clickCoordinate)
#     defineYaxis(clickRegistered,clickCoordinate)
#     getDataPoints(clickRegistered,clickCoordinate)

    # print(data)
#

class uiProcess(threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        global clickCoordinate
        global clickRegistered
        global exitFlag
        print ("Starting " + self.name)
        self.plots()
        while not exitFlag:
            time.sleep(0.001)
            pass
        # self.defineYaxis()
        # self.getDataPoints()
        print("Exiting " + self.name)


    def plots(self):
        global clickCoordinate
        global clickRegistered
        global exitFlag
        fig = plt.figure(figsize=(10,10))
        # ax = fig.add_subplot(111)

        #ax = plt.subplots()
        # clickStatus = 0

        cid = fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.imshow(img)
        # defineXaxis()
        # plt.show()

    def onclick(self, event):
        global clickCoordinate
        global clickRegistered
        global exitFlag
        try:
            print('Click registered at %d, %d' %(event.x, event.y))

            # data.append([event.x, event.y])
            # choice = input("More data available? (y/n)")

            clickCoordinate = [event.x, event.y]
            # print(clickCoordinate)
            clickRegistered = True

            # clickStatus = 1

        except Exception as e:
            print("Error! - ", e)


def plots():
    global clickCoordinate
    global clickRegistered
    global exitFlag
    global drawCallPending
    global drawCallQueue

    global xAxis
    global yAxis
    global data

    plt.ion()

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)

    #ax = plt.subplots()
    # clickStatus = 0

    cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    plt.imshow(img)
    # defineXaxis()
    plt.draw()
    # plt.show()

    while not exitFlag:
        if drawCallPending:
            while not drawCallQueue.empty():
                fromQueue = drawCallQueue.get()
                print(fromQueue)
                print(xAxis)
                line = fromQueue[1]
                exec(fromQueue[0])
                drawCallQueue.task_done()
                plt.draw()
            drawCallPending = False

        plt.pause(10)

    plt.show()

def onclick(event):
    global clickCoordinate
    global clickRegistered
    global exitFlag
    try:
        print('Click registered at %d, %d' %(event.x, event.y))
        print('Data at Click = %d, %d' %(event.xdata, event.ydata))

        # data.append([event.x, event.y])
        # choice = input("More data available? (y/n)")

        clickCoordinate = [event.xdata, event.ydata]
        # print(clickCoordinate)
        clickRegistered = True

        # clickStatus = 1

    except Exception as e:
        print("Error! - ", e)


def findTransformationMat():
    cv


if __name__ == '__main__':

    script_path = os.path.dirname(os.path.abspath( __file__ ))

    imageFileName = 'transm1.jpg'
    imageFileName = os.path.join(script_path, imageFileName)

    img = mpimg.imread(imageFileName)
    data = []

    xAxis = []
    yAxis = []


    # clickRegistered = mp.Value('i', 0)
    clickRegistered = False

    # clickCoordinate = mp.Array('i', [0,0])
    clickCoordinate = []

    exitFlag = False
    drawCallPending = False
    drawCallQueue = Queue(maxsize=0)

    thread1 = dataProcess(1, "data")
    thread2 = uiProcess(2, "UI")

    thread1.start()
    # thread2.start()


    # dataProcess = mp.Process(target=getData, args=(clickRegistered,clickCoordinate))
    # dataProcess.start()

    # plotProcess = mp.Process(target=plots,args=(clickRegistered,clickCoordinate))
    # plotProcess.start()

    # getData(clickRegistered,clickCoordinate)

    plots()


    #load image
    # define axes
        # get n points on each axis
    # define points
    # save mat