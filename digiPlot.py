import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import multiprocessing as mp
import os

script_path = os.path.dirname(os.path.abspath( __file__ ))

imageFileName = 'transm1.jpg'
imageFileName = os.path.join(script_path, imageFileName)



#import matplotlib.pyplot as plt

img = mpimg.imread(imageFileName)
data = []
clickRegistered = mp.Value('i', 0)
clickCoordinate = mp.Array('i', [0,0])
xAxis = []
yAxis = []

def getData(clickRegistered,clickCoordinate):
    defineXaxis(clickRegistered,clickCoordinate)
    defineYaxis(clickRegistered,clickCoordinate)
    getDataPoints(clickRegistered,clickCoordinate)

def defineYaxis(clickRegistered,clickCoordinate):
    print("Pick points on Y axis...")
    choice = "y"
    while choice == 'y':
        if clickRegistered == 1:
            value = input('What is the Y value? : ')
            yAxis.append([clickCoordinate, value])
            clickRegistered = False
            choice = input("More axis points available? (y/n)")

    print(yAxis)

def defineXaxis(clickRegistered,clickCoordinate):
    print("Pick points on X axis...")
    choice = "y"
    while choice == 'y':
        if clickRegistered == 1:
            value = input('What is the X value? : ')
            xAxis.append([clickCoordinate, value])
            clickRegistered = False
            choice = input("More axis points available? (y/n)")

    print(xAxis)

def getDataPoints(clickRegistered,clickCoordinate):
    print("Pick points on the curve...")

    choice = "y"
    while choice != "n":
        if clickRegistered == 1:
            data.append(clickCoordinate)
            clickRegistered = False
            choice = input("More data available? (y/n)")

    print(data)

def onclick(event):
    try:
        print('%d, %d' %(event.x, event.y))

        data.append([event.x, event.y])


        # choice = input("More data available? (y/n)")

        # clickCoordinate = [event.x, event.y]
        # clickRegistered = True

    except Exception as e:
        print("Error! - ", e)


def plots(clickRegistered,clickCoordinate):

    fig = plt.figure(figsize=(10,10))
    # ax = fig.add_subplot(111)

    #ax = plt.subplots()
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.imshow(img)
    # defineXaxis()
    plt.show()

if __name__ == '__main__':

    dataProcess = mp.Process(target=getData, args=(clickRegistered,clickCoordinate))
    dataProcess.start()

    plotProcess = mp.Process(target=plots,args=(clickRegistered,clickCoordinate))
    plotProcess.start()

    # getData(clickRegistered,clickCoordinate)

    # plots(clickRegistered, clickCoordinate)


    #load image
    # define axes
        # get n points on each axis
    # define points
    # save mat