#Full FB code here
# Much of this code is copied from this article:
# https://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117
#Coordinates 
#All coordinates assume a screen resolution of 1920 x 1080, and Chrome 
#Without toolbar enabled. 
#x_pad = 69
#y_pad = 149

from ctypes import windll, c_int, c_uint, c_char_p, c_buffer
from PIL import ImageGrab,Image,ImageFilter,ImageOps
from mss import mss
sct = mss()
import cv2
import pytesseract
import os
import time
import numpy
import win32api, win32con
from win32con import *
import win32gui
import datetime
from numpy import *
import win32com.client
from skimage import img_as_float
from skimage.metrics import structural_similarity as ssim
from PIL import Image 
from struct import calcsize, pack
import pyautogui
gdi32 = windll.gdi32

#################################################################

###############  Code set up secttion

################################################################

## set your own directory
os.chdir('C:\\Users\\mppeb\\Documents\\FBPython')


## example: Your PC username is MarkAnthony, and you saved the script directly in the Documents folder. So you need to change the script to say
# os.chdir('C:\\Users\\MarkAnthony\\Documents')


####Path to tesseract installation folder.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


#This variable is the number of seconds that the program should wait when switching locations within Hero wars.
setLoadTime = 10






####################################



# Win32 functions
CreateDC = gdi32.CreateDCA
CreateCompatibleDC = gdi32.CreateCompatibleDC
GetDeviceCaps = gdi32.GetDeviceCaps
CreateCompatibleBitmap = gdi32.CreateCompatibleBitmap
BitBlt = gdi32.BitBlt
SelectObject = gdi32.SelectObject
GetDIBits = gdi32.GetDIBits
DeleteDC = gdi32.DeleteDC
DeleteObject = gdi32.DeleteObject

# Win32 constants
NULL = 0
HORZRES = 8
VERTRES = 10
SRCCOPY = 13369376
HGDI_ERROR = 4294967295
ERROR_INVALID_PARAMETER = 87


# Globals
# ------------------

#Put in the distance from the top righthand corner
#to the beginning of the hero wars app on your computer.
#To measure it, take a screen shot, and open up
#Microsoft Paint. Turn on the grid view, and you'll be
#able to see distance in pixels.

lib = windll.user32
user32 = windll.user32
#this process makes the program aware of your display
#scaling, that way it can control for it. 
user32.SetProcessDPIAware()

### Function to extract text
def genRegion(loc1, loc2):
    locR = {'top': y_pad + loc1[1] , 'left': (x_pad + loc1[0]),
                  'width': (loc2[0]-loc1[0]), 'height': (loc2[1]-loc1[1])}
    return locR

def extractText(region, invert):
    img1 = sct.grab(region)
    #img1 = ImageGrab.grab(bbox = (int(0.0048*height),int(0.184*height),int(0.4436*width),int(0.6478*height)),
                        #  include_layered_windows=False, all_screens=True)
   # hsv = cv2.cvtColor(numpy.array(img1), cv2.COLOR_BGR2HSV)
    #mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))
    #imask = mask>0
    #green = numpy.zeros_like(img1, numpy.uint8)
    #green[imask] = hsv[imask]
    img2 = cv2.cvtColor(numpy.array(img1), cv2.COLOR_BGR2GRAY)
    if invert:
        img2 = cv2.bitwise_not(img2)
    text = pytesseract.image_to_string(img2,lang="eng")
    return text.replace("\n"," ")

 
def leftClick():
    tmp1 = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print("Click.")
    tmp2 = win32api.GetCursorPos()
    if tmp1 != tmp2:
        user_choice = input("It looks like you moved your mouse. The autoplay script has automatically paused. Would you like to resume? y/n")
        while(not (user_choice in "y" or user_choice in 'n')):
            user_choice = input("It looks like you moved your mouse. The autoplay script has automatically paused. Would you like to resume? y/n")
        if user_choice in "y":
            print("Let's continue")
        elif user_choice in "n":
            user_choice = "y"
            quit()
        
            
#completely optional. But nice for debugging purposes.

def minimizeScreen():
    #Pressed Windows + Down
    win32api.keybd_event(0x91, 0,0,0)
    win32api.keybd_event(0x28, 0,0,0)
    time.sleep(.05)
    win32api.keybd_event(0x91,0 ,win32con.KEYEVENTF_KEYUP ,0)
    win32api.keybd_event(0x28, 0,win32con.KEYEVENTF_KEYUP ,0)
    time.sleep(0.1)

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print('left Down')
         
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print('left release')

def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
    
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x,y)

def grab(pos,extra):
    box = (x_pad + pos[0],y_pad+pos[1],x_pad+ pos[0]+extra[0],y_pad+ pos[1]+extra[1])
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print(a)
    return a
    
#Takes in "image" files from Pillow (PIL)
#Compares two images and finds the structural similarity
def simImages(image1, image2):
    img1 = img_as_float(image1)
    img2 = img_as_float(image2)
    dmax = 0
    if img1.max() > img2.max():
        dmax = img1.max()
    else:
        dmax = img2.max()
    dmin = 0
    if img1.min() > img2.min():
        dmin = img1.min()
    else:
        dmin = img2.min()
    ssim_const = ssim(img1,img2,
                  data_range=dmax - dmin, multichannel = True)
    return ssim_const
#tests if the initial pop up is there, 
def PopUp(initial):
    current = screenGrab()
    if simImages(initial,current) > .50:
        win32api.keybd_event(0x1B, 0,0,0)
        time.sleep(.05)
        win32api.keybd_event(0x1B,0 ,win32con.KEYEVENTF_KEYUP ,0)
        time.sleep(0.1)


#Exits page
def ExitScreen(typeEsc):

    mainExit = (int(0.96*width),int(0.02*height))
    secondExit = (int(0.92*width),int(0.12*height))
    chestExit = (int(0.95*width), int(0.136*height))
    dailyExit = (int(0.81*width),int(0.17*height))
    messageExit = (int(0.81*width),int(0.085*height))
    raidExit1 = (int(0.95*width), int(0.078*height))
    raidRewardExit = (int(0.87*width), int(0.144*height))
    bonusExit = (int(0.82*width), int(0.11*height))
    towerExit = (int(0.95*width), int(0.05*height))
    towerTopExit = (int(0.735*width), int(0.12*height))
    dailyChestExit = (int(0.777*width), int(0.1445*height))
    oracleExit = (int(0.9*width), int(0.15*height))
    
    if 'Main' in typeEsc:

        mousePos(mainExit)
        
    elif "SecondDaily" in typeEsc:

        mousePos(secondExit)

    elif "DailyChest" in typeEsc:

        mousePos(dailyChestExit)
     
    elif "Chest" in typeEsc:

        mousePos(chestExit)

    elif "RaidReward" in typeEsc:

        mousePos(raidRewardExit)

    elif "Daily" in typeEsc:

        mousePos(dailyExit)

    elif "Messages" in typeEsc:

        mousePos(dailyExit)

    elif "Friends" in typeEsc:

        mousePos(bonusExit)

    elif "Raid" in typeEsc:

        mousePos(raidExit1)

    elif "Bonus" in typeEsc:

        mousePos(bonusExit)
  
    elif "TowerTop" in typeEsc:

        mousePos(towerTopExit)

    elif "Tower" in typeEsc:

        mousePos(towerExit)
    elif "Oracle" in typeEsc:

        mousePos(oracleExit)

    leftClick()
    time.sleep(0.5)
    

#Clicks escape n times
#def EscHome(n):
#    iter1 = 0
#    while iter1 < n:
#        print(str(n))
#        win32api.keybd_event(0x1B, 0,0,0)
#        time.sleep(.05)
#        win32api.keybd_event(0x1B,0 ,win32con.KEYEVENTF_KEYUP ,0)
#        time.sleep(0.1)
#        iter1+=1
                
#Compares a position to a previously recorded image, and clicks if it's the same.
#Great for recognizing if the button says"Free" or you have to pay with diamonds.
#return 1 if clicked, 0 if not (true or false
def Avail(orig,pos,size):
    button = boxgrab(pos,size)
    print( "Similarity is " + str(simImages(button,orig)))
    if simImages(button,orig) > 0.45:
        mousePos(pos)
        time.sleep(0.1)
        leftClick()
        return 1
    return 0

#For the tower - identifying objects or moving to the next level
def NextThing(pos):
    #im1 = screenGrab()
    mousePos(pos[0])
    leftClick()
    time.sleep(0.5)
    mousePos(pos[1])
    leftClick()
    #im2 = screenGrab()
    #if simImages(im1, im2) > .80:
       
    time.sleep(1)

#Checks if the game is stuck. If so, will refresh if refresh = 1. Will do so n times
    #If refresh = 0, it'll just check if the game is stuck and return 1 if so, or 0 if not.
def refreshScreen(im1, refresh, n):
    im2 = screenGrab()
    if simImages(im1,im2) > 0.70 and refresh == 0:
        return 1
    elif simImages(im1,im2) < 0.70 and refresh == 0:
        return 0
    noInternet = Image.open(os.getcwd() + '\\noInternet' + '.png')
    iter1 = 0
    iter2 = 0
    while simImages(im1,im2) > 0.70 and iter1 < n :
        if iter1%5 == 0:
            mousePos((42,-87)) #refresh button location.
            leftClick()
            print("Refreshing..")
            iter1 += 1
            noInternet1 = boxgrab((449,93),(400,400))
            #In case internet's down, it just waits.
            while simImages(noInternet1,noInternet) > 0.90 and iter2 <50 :
                iter2+=1
                mousePos((42,-87)) #refresh button location.
                leftClick()
                time.sleep(15)
                print("No Internet. Refreshing...")
        time.sleep(5)
        im2 = screenGrab()

#Searches for saved image on the screen of a given size.
# Clicks it if it's available.
#The grain is how small of an area it should iterate over.
#10 pixels? 20 pixels?
def SearchForImage(orig,size,grain):
    pos = (0,0)
    fullscreen = screenGrab()
    width = fullscreen.size[0]-size[0]
    height = fullscreen.size[1]-size[1]

    while Avail(orig,pos,size) == 0:
        if pos[0] + grain < width :
            pos[0] += grain
        elif pos[0] + grain > width:
            pos[1] += grain
        else:
            print("Search Failed!")
            break

#Collect quests
def CollectQuests():
    mousePos((int(0.2*width),int(0.0457*height)))
    time.sleep(0.75)
    leftClick()
    time.sleep(0.75)

    text = extractText(genRegion((int(0.665*width),int(0.287*height)),(int(0.748*width),int(0.34*height))), TRUE)
    iter1 = 0
    while( 'Complete' in text) and iter1 < 50:
        iter1 += 1
        mousePos((int(0.7*width),int(0.3*height)))
        leftClick()
        time.sleep(1)
        text = extractText(genRegion((int(0.665*width),int(0.287*height)),(int(0.748*width),int(0.34*height))), TRUE)
        
    ExitScreen('Daily')

def Fight(Valk):
    for i in (0,1,2,3,4):
        mousePos((int((0.247+i*0.106)*width),int(0.344*height)))
        leftClick()
        time.sleep(0.5)
    for i in (0,1,2,3,4):
        mousePos((int((0.247+i*0.106)*width),int(0.344*height)))
        leftClick()
        time.sleep(0.5)

    #Start fight
    mousePos((int(0.864*width),int(0.894*height)))
    leftClick()
    time.sleep(3)
    #activate auto
    mousePos((int(0.927*width),int(0.845*height)))
    leftClick()
    #fighting = screenGrab()
    if Valk:
        mousePos((int(0.927*width),int(0.929*height)))
        leftClick()
    #Check if done fighting every 5 seconds, up to 24 times. 
    iter1 = 0;
    okBox = genRegion((int(0.451*width),int(0.774*height)),(int(0.542*width),int(0.830*height)))
    text2 = extractText(okBox, TRUE)
    
    while not 'OK' in text2 and iter1 < 60:
        print("Loop " + str(iter1))
        time.sleep(2)
        iter1 +=1
        text2 = extractText(okBox, TRUE)

    if 'OK' in text2:
        mousePos((int(0.51*width),int(0.797*height)))
        leftClick()
        time.sleep(1)
    else:
        return(iter1)
    return iter1


def newCoord():
    pos = win32api.GetCursorPos()
    return ((pos[0]-x_pad)/width,(pos[1]-y_pad)/height)

def collectDaily():
    time.sleep(2)
    mousePos((int(0.217*width), int(0.185*height)))
    time.sleep(0.2)
    leftClick()
    time.sleep(1)

    #Click on all the daily bonus for the day -
    today = datetime.datetime.today().day

    #Here's the list of coordinates for each day
    #
    Columns = (int(0.362*width),int(0.447*width),int(0.587*width),int(0.698*width),int(0.809*width))
    Rows = (int(0.333*height),int(0.541*height),int(0.749*height))

    #Below is testing code, to make sure your positions for each day of the month are right.
    '''
    for x in list(range(17,31)):
        today =x
        ColNum = int((today-1)%5)
        RowNum = int((today-1-ColNum)/5)
        skip = 1
        if RowNum < 2:
            mousePos((Columns[ColNum],Rows[RowNum]))
        elif RowNum < 3:
            RowNum = RowNum - 1
            mousePos((Columns[ColNum],Rows[RowNum]))
        elif RowNum < 4:
            print("Row Number is " + str(RowNum))
            mousePos((426,340))
            #leftClick()
            RowNum = RowNum - 2
            mousePos((Columns[ColNum],Rows[RowNum]))
        elif RowNum < 5:
            mousePos((426,340))
            #leftClick()
            time.sleep(0.5)
            RowNum = RowNum - 3
            mousePos((Columns[ColNum],Rows[RowNum]))
        elif RowNum < 6:
            RowNum = RowNum - 3
            mousePos((Columns[ColNum],Rows[RowNum]))
            #leftClick()
            time.sleep(1)
            RowNum = RowNum - 1
            mousePos((Columns[ColNum],Rows[RowNum]))
            #leftClick()
            time.sleep(1)
        elif RowNum < 7:
            #mousePos((426,340))
           #leftClick()
            RowNum = RowNum - 4
            mousePos((Columns[ColNum],Rows[RowNum]))
        else:
            print("Error on daily bonus!")
            skip=0
        time.sleep(1)
        win32api.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, 120, 0)
        time.sleep(0.5)
    '''

    # So basically, every 5th day, you have to move down to the next row.
    # The remainder will tell you which column to use.
    # So take the day and subtract 1, because pyhton is 0-indexed
    # find the remainder. of the day and 5 (# of columns)
    # Substract the day number by the remainder -
    # and divide by 5 to find the column number

    ColNum = int((today-1)%5)
    RowNum = int((today-1-ColNum)/5)
    skip = 1
    if RowNum < 2:
        mousePos((Columns[ColNum],Rows[RowNum]))
    elif RowNum < 3:
        RowNum = RowNum - 1
        mousePos((Columns[ColNum],Rows[RowNum]))
    elif RowNum < 4:
        print("Row Number is " + str(RowNum))
        mousePos((426,340))
        leftClick()
        RowNum = RowNum - 2
        mousePos((Columns[ColNum],Rows[RowNum]))
    elif RowNum < 5:
        mousePos((426,340))
        leftClick()
        time.sleep(0.5)
        RowNum = RowNum - 3
        mousePos((Columns[ColNum],Rows[RowNum]))
    elif RowNum < 6:
        RowNum = RowNum - 3
        mousePos((Columns[ColNum],Rows[RowNum]))
        leftClick()
        time.sleep(1)
        RowNum = RowNum - 1
        mousePos((Columns[ColNum],Rows[RowNum]))
        leftClick()
        time.sleep(1)
    elif RowNum < 7:
        mousePos((426,340))
        leftClick()
        RowNum = RowNum - 4
        mousePos((Columns[ColNum],Rows[RowNum]))
    else:
        print("Error on daily bonus!")
        skip=0
        
    if skip:
        time.sleep(1)
        leftClick()
        time.sleep(1)

    time.sleep(2)
    text = extractText(genRegion((int(0.462*width),int(0.73*height)),(int(0.542*width),int(0.77*height))), TRUE)
    if 'Collect' in text:
        mousePos((int(0.5*width),int(0.75*height)))
        leftClick()
        time.sleep(1)

    text = extractText(genRegion((int(0.47*width),int(0.51*height)),(int(0.53*width),int(0.54*height))), TRUE)
    if 'OK' in text:
        mousePos((int(0.5*width),int(0.53*height)))
        leftClick()
        time.sleep(1)

    time.sleep(0.5)

    ### Get daily skins
    skins = (int(0.152*width),int(0.367*height))
    mousePos(skins)
    time.sleep(1)
    leftClick()
    time.sleep(1)
    #Check if free skin available

    #text = extractText(genRegion((int(0.465*width),int(0.606*height)),(int(0.547*width),int(0.638*height))), TRUE)
    #if 'Collect' in text:
    #    mousePos((int(0.5*width),int(0.625*height)))
    #    leftClick()
    #    time.sleep(1)
    #    EscHome(2)
    #else:
    mousePos((int(0.5*width),int(0.625*height)))
    leftClick()

    ExitScreen('SecondDaily')
    time.sleep(0.5)

def collectMessages():
    messages = (int(0.22*width),int(0.115*height))
    mousePos(messages) #Click on messages
    time.sleep(1)
    leftClick()
    time.sleep(1)

    collectMessages = (int(0.507*width),int(0.835*height))
    mousePos(collectMessages) #click on "Collect all"
    time.sleep(1)
    leftClick()
    GetAll = (int(0.504*width),int(0.768*height))
    mousePos(GetAll) #click on collect all again
    time.sleep(1)
    leftClick()

    time.sleep(2)

    #Check if any messages left, and collect those - like from guild wars or other.
    #Color = get_main_color((939,179),buttonExtra) #See if there's anything to collect
    #iter1 = 0
    #while iter1 < 10:
    #    iter1 += 1
    #    time.sleep(1)
    #    text = extractText(genRegion((int(0.68*width),int(0.238*height)),(int(0.76*width),int(0.273*height))), TRUE)
    #    if 'Read' in text:
    #             mousePos((int(0.70*width),int(0.25*height)))
    #             leftClick()
    #             time.sleep(1)
    #             text = extractText(genRegion((int(0.463*width),int(0.803*height)),
    #                                          (int(0.53*width),int(0.838*height))), TRUE)
    #             if 'Collect' in text:
    #                 mousePos((int(0.5*width),int(0.82*height)))
    #                 leftClick()
    #    else:
    #        print("Unknown message!")
    #        EscHome(current,1)
    #    time.sleep(1)

    leftClick()
    time.sleep(1)
    ExitScreen('Bonus')

def openDailyChest():
    dailyChest = (int(0.655*width),int(0.79*height))
    mousePos((int(0.23*width),int(0.690*height)))
    leftClick()
    #Load the image of when the button is free
    time.sleep(1)
    text = extractText(genRegion((int(0.61*width),int(0.78*height)),(int(0.71*width),int(0.83*height))), TRUE)
    if 'Open' in text:
        mousePos((int(0.65*width),int(0.82*height)))
        leftClick()
        time.sleep(3)


def processGifts():
    gifts = (int(0.723*width),int(0.857*height))
    mousePos(gifts) #click on gifts
    leftClick()
    time.sleep(0.5)
    text = extractText(genRegion((int(0.43*width),int(0.51*height)),(int(0.57*width),int(0.58*height))), TRUE)
    if 'Send' in text:
        mousePos((int(0.43*width),int(0.51*height)))
        leftClick()
        time.sleep(1)
    else:
        ExitScreen('Bonus')
    time.sleep(2)

def raidTitanValley(titanValley):
    titanCup = (int(0.4*width), int(0.46*height)) #to enter cup and get rewards for theweek
    tournElem = (int(0.2*width), int(0.29*height)) #to enter tournament
    raidTitan = (int(0.635*width), int(0.776*height)) #To raid a level of the tournament
    contRaidTitan = (int(0.5*width), int(0.77*height)) #continue/confirm raid.

    mousePos(titanValley) #Get to titan valley
    leftClick()
    time.sleep(5)
    #titans = screenGrab()
    #put wait time in here
    #Check if it's Saturday and collect tournament rewards
    DayOfTheWeek = datetime.datetime.weekday(datetime.datetime.today())
    if DayOfTheWeek == 6:
        mousePos(titanCup) #Go to the temple
        leftClick()
        time.sleep(0.5)
        mousePos((633,563))
        leftClick()
        time.sleep(0.5)
        ExitScreen('Raid') #backto the valley...which is actually floating clouds and not a valley.
    else:    
        mousePos(tournElem) #Open up tournament of the elements
        leftClick()
        time.sleep(2)

        text = extractText(genRegion((int(0.608*width),int(0.756*height)),(int(0.674*width),int(0.792*height))), TRUE)

        while 'Raid' in text:
            
            mousePos(raidTitan)
            leftClick()
            time.sleep(0.75)

            text = extractText(genRegion((int(0.476*width),int(0.752*height)),(int(0.53*width),int(0.785*height))), TRUE)
            if 'Raid' in text:
                mousePos(contRaidTitan) #Confirm Raid button
                leftClick()
                time.sleep(4)

                mousePos((int(0.5*width), int(0.828*height)))
                leftClick()
                leftClick()
                time.sleep(2)
                
                text = extractText(genRegion((int(0.423*width),int(0.648*height)),(int(0.573*width),int(0.677*height))), TRUE)
                if 'Claim Reward' in text:
                    mousePos((int(0.5*width), int(0.655*height)))
                    leftClick()
                    time.sleep(1)

                time.sleep(2)
                text = extractText(genRegion((int(0.608*width),int(0.756*height)),(int(0.674*width),int(0.792*height))), TRUE)
                
            else:
                text = "NULL"
                

        time.sleep(3)
        mousePos((int(0.92*width), int(0.685*height))) #Get to rewards chest for titans
        leftClick()
        time.sleep(2)
        text = extractText(genRegion((int(0.446*width),int(0.774*height)),(int(0.53*width),int(0.83*height))), TRUE)
        if 'Claim' in text:
            mousePos((int(0.49*width), int(0.798*height)))
            leftClick()
            #text = extractText(genRegion((int(0.463*width),int(0.614*height)),(int(0.537*width),int(0.648*height))), TRUE)
            
            mousePos((int(0.5*width), int(0.655*height)))
            leftClick()
            time.sleep(3)
            #if 'Collect' in text:
            #    
            #    
           # else:
            #    ExitScreen('RaidReward')
        else:
            ExitScreen('RaidReward')
    ExitScreen('Raid')
    ExitScreen('Raid')

def dungeonCrawl():

    dungeon = ((int(0.711*width), int(0.35*height)),(int(0.494*width), int(0.36*height)))

    iter1 =0

    while iter1 < 60:
        iter1 += 1

        text = extractText(genRegion((int(0.43*width),int(0.71*height)),(int(0.624*width),int(0.76*height))), TRUE)

        NextThing(dungeon)#Open up next fight
        time.sleep(3)

        text = extractText(genRegion((int(0.43*width),int(0.71*height)),(int(0.624*width),int(0.76*height))), TRUE)
        text2 = extractText(genRegion((int(0.675*width),int(0.72*height)),(int(0.767*width),int(0.77*height))), TRUE)
        text3 = extractText(genRegion((int(0.227*width),int(0.252*height)),(int(0.299*width),int(0.315*height))), TRUE)
        text4 = extractText(genRegion((int(0.517*width),int(0.62*height)),(int(0.65*width),int(0.66*height))), TRUE)
        text5 = extractText(genRegion((int(0.449*width),int(0.72*height)),(int(0.54*width),int(0.768*height))), TRUE)
        if 'Accept' in text or 'fate' in text or 'this' in text:
            mousePos((int(0.5*width),int(0.73*height)))
            leftClick()
            time.sleep(2)
        elif 'Attack' in text2 :
            
            mousePos((int(0.7*width),int(0.75*height)))
            leftClick()
            time.sleep(2)
            text = extractText(genRegion((int(0.43*width),int(0.71*height)),(int(0.624*width),int(0.76*height))), TRUE)
            text2 = extractText(genRegion((int(0.517*width),int(0.62*height)),(int(0.65*width),int(0.66*height))), TRUE)
            
            if 'Accept' in text or 'fate' in text or 'this' in text:
                mousePos((int(0.5*width),int(0.73*height)))
                leftClick()
            elif 'Fight' in text2 or 'on your' in text2 or 'own' in text2:
                iter1 = 50
            else:
                mousePos((int(0.5*width),int(0.73*height)))
                leftClick()
                iter2 = Fight(Valk)
                if iter2 == 48:
                   break #if the victory screen did not pop up, then break the loop and end the dungeon.

        elif 'Activate' in text3:
            mousePos((int(0.25*width),int(0.27*height)))
            leftClick()
            time.sleep(5)
            mousePos((int(0.69*width),int(0.68*height)))
            leftClick()
            time.sleep(4)
        elif 'Fight' in text2 or 'on your' in text2 or 'own' in text2:
            iter1 = 100
        elif 'Attack' in text5 :
            mousePos((int(0.5*width),int(0.73*height)))
            leftClick()
            iter2 = Fight(Valk)
            if iter2 == 60:
                break


            
def clearTower():
    #click instant clear - but go through manually
    mousePos((int(0.468*width), int(0.489*height)))
    time.sleep(1)
    leftClick()
    time.sleep(2)
    #Click on choose chests
    mousePos((int(0.3*width), int(0.696*height)))
    leftClick()
    time.sleep(1)
    lvl = 0
    
    while lvl < 55:
        #check for chest on the right side
        #im1 = screenGrab()
        mousePos((int(0.695*width), int(0.508*height)))
        leftClick()
        time.sleep(1)
        #im2 = screenGrab()
        #check for chest on the right side
        mousePos((int(0.334*width), int(0.517*height)))
        leftClick()
        time.sleep(1)
        #if simImages(im1,im2) > 0.90:

        #open a chest
        mousePos((int(0.22*width), int(0.63*height)))
        leftClick()
        time.sleep(1)
        #Proceed to the next level
        mousePos((int(0.829*width), int(0.837*height)))
        leftClick()
        time.sleep(2)


        text = extractText(genRegion((int(0.156*width+-18),int(0.386*height-18)),
                                     (int(0.156*width+18),int(0.386*height+18))), TRUE)
        if '50' in text:
            lvl = 55
            
        lvl = lvl + 1
                

    #check for chest last chest
    mousePos((int(0.8*width), int(0.5*height)))
    leftClick()
    time.sleep(2)
    #open a chest
    mousePos((int(0.22*width), int(0.63*height)))
    leftClick()
    time.sleep(2)

    #Exit chest screen
    ExitScreen("Chest")


    
    mousePos((int(0.05*width), int(0.0721*height))) # Collect extra skulls
    leftClick()
    time.sleep(2)
    mousePos((int(0.5*width), int(0.657*height)))#second click to collect
    leftClick()
    time.sleep(2)

    mousePos((int(0.126*width), int(0.915*height))) # Get tower point rewards
    time.sleep(2)
    leftClick()
    time.sleep(2)
    mousePos((int(0.489*width), int(0.854*height))) #collect all
    leftClick()

    time.sleep(1)
    #Exit tower screen
    ExitScreen('TowerTop')
    time.sleep(0.5)
    ExitScreen('Tower')
    
def main():
   pass

################################## Ask for different user options

done = 'n'
while done == 'n':
    user_choice = input("Do you have Hero Wars open to full screen on your primary monitor with this prompt on top of it? y/n If you only have one screen, press 'y'")
    if user_choice == "y":
        done = 0
    else:
        print("Please open Hero Wars on your primary monitor and move this program on top of it.")


done = 'n'
while done == 'n':   
    user_choice = input("Do you have the Valkyrie boost? y/n")
    if user_choice == "y" or user_choice == "Y":    
        Valk =  1#Set to 1 if you have Valkyrie, and 0 if not.
        done =0 
    elif user_choice == "n" or user_choice == "N":
        Valk = 0
        done = 0
    else:
        print("Sorry,wrong input. Try again")

print('Excellent! You have Hero Wars open right behind this program on your primary monitor. You are ready to go.')
size = pyautogui.size()

if 14*size.height/9 < size.width:
    height = size.height
    width = round(14*height/9)
    y_pad = 0
    x_pad = round((size.width - width)/2)
    
else:
    width = size.width
    height = round(width*9/14)
    x_pad = 0
    y_pad = round((size.height - height)/2)

#Regular click points
buttonExtra = (int(0.04004*width),int(0.04004*height))
guild = (int(0.058*width), int(0.851*height))

done = 'n'
while done == 'n':
    print('What autoplay would you like to do?')
    print('Clear Tower - 1')
    print('Crawl the Dungeon- 2')
    print('Raid Titan Valley  - 3')
    print('Collect Daily Rewards - 4')
    print('Quit this program - 5')
          
    user_choice = input("Type in the number for your selection:")
    if user_choice == "1":

        minimizeScreen()
        tower = (int(0.861*width),int(0.205*height))
        mousePos(tower) #Enter said tower
        leftClick()
        time.sleep(setLoadTime/2)
        clearTower()

        
    elif user_choice == "2":
        minimizeScreen()
        mousePos(guild) #Get to guild
        leftClick()
        time.sleep(setLoadTime)

        mousePos((int(0.617*width), int(0.675*height)))
        leftClick()
        time.sleep(2)

        mousePos((int(0.135*width), int(0.5*height)))
        leftClick()
        time.sleep(2)

        mousePos((int(0.049*width), int(0.082*height)))
        leftClick()
        time.sleep(0.5)
        if Valk:
            mousePos((int(0.817*width), int(0.322*height)))
            leftClick()
            time.sleep(0.5)

        mousePos((int(0.817*width), int(0.442*height)))
        leftClick()
        time.sleep(0.75)
        mousePos((int(0.817*width), int(0.565*height)))
        leftClick()
        time.sleep(0.75)
        mousePos((int(0.817*width), int(0.694*height)))
        leftClick()
        time.sleep(0.75)

        ExitScreen('Oracle')        

        dungeonCrawl()

        ExitScreen('Main')
        time.sleep(0.2)
        ExitScreen('Main')
        time.sleep(0.5)

        mousePos(guild) #Get to guild
        leftClick()
        time.sleep(10)

    elif user_choice == "3":
        minimizeScreen()
        #####Change scenes
        guild = (int(0.058*width), int(0.851*height))
        mousePos(guild) #Get to guild
        leftClick()
        time.sleep(setLoadTime)

        titanValley = (int(0.324*width), int(0.33*height))
        raidTitanValley(titanValley)
        time.sleep(3)

        mousePos(guild) #Get to guild
        leftClick()
        time.sleep(10)

    elif user_choice == "4":
        
        processGifts()
        collectMessages()
        collectDaily()
        openDailyChest()
        

        time.sleep(1)
        

    elif user_choice == "5":
        quit()



