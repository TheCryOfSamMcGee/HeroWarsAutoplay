# HeroWarsAutoplay
Scripts for auto-playing portions of Hero Wars

Hello and welcome! I've been playing around with some python scripts so that my computer can grind through Hero Wars while I make my coffee. I've been using them for the past year to race through the tower, and dungeon portions without my involvement. That being said, this script works by controlling the mouse on your computer, and if you have pop-ups or other unusual stuff screen-wise, it will click on those, so use it at your own risk. If you want the script to stop quickly, just move your mouse - it'll detect that and pause. This script is meant to be used at your own risk, so be smart. If you are worried about it accidentally spending diamonds, then monitor it. I've added a setting to account for slower internet (see below), and if your internet is too slow, the script can mess up and spend diamonds accidentally.

Specifically, I've seen the script get confused, think it was moving through the tower during the loading screen, and accidentally exit the tower, but still think it was moving through the tower. When it went to click on the next chest in the tower, it would click on the hero's chest and spend diamonds to open it. So yeah, adjust the loading time. 

<br />
<br />

## Running the script

The script is designed to navigate Hero Wars from the full screen view. From the main page of Hero Wars, look at the bottom right corner and you'll see two green buttons. The left one will make Hero Wars run full screen. From there, the script will figure everything else out. Just follow the prompts. 

Just make sure to run the script starting from the Hero Wars home page opened to the full screen view. 


<br />
<br />
<br />


## Installation
If you want to install and run this script, you need to install python with all the libraries imported at the beginning of the script, as well as pytesseract Once Pytesseract is installed, then tell the script where to find it. This is found at the beginning of the script and looks like this. 

#### set your own directory
os.chdir('C:\\Users\\JohnDoe\\Documents\\FBPython')

####Path to pytesseract install
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

The other variable you can set at the beginning is setLoadTime:
#This variable is the number of seconds that the program should wait when switching locations within Hero wars. This is important because slower internets can slow down the load times, and mess up the script. 
setLoadtime = 10


<br />
<br />



### Current limitations:
- Right now, the script is designed for people who are level 130, and doesn't work if you can't skip the battles in the tower. 
- It only runs on Windows, because I do not have a Mac to play around with, and I cannot afford one.
- There isn't a way to update the load

If you have questions, feel free to post it in the issues tab. If you want to see an improvement, mark your post an enhancement. 


<br />
<br />
<br />



## Donations:

I do have a full-time job, but my ex-wife left and tried to take our toddler son too. I made sure she failed, but I don't have much free time or cash now from the legal battle, so if you like these scripts, please feel free to donate! Thank you again for your support.


| Paypal | CashApp |
| ------ | ------- |
|[![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?business=CGHXKUED9CJHW&no_recurring=0&currency_code=USD)
![image](https://user-images.githubusercontent.com/122340776/211473862-30af57fa-7b5e-46f6-a020-9dcfb3334695.png) |![image](https://user-images.githubusercontent.com/122340776/211480358-098f34b7-1b21-42cb-a174-177ef20236df.png)|



Feedback:

Please feel free to leave comments via the 'Issues' tab. If you want to see any new features, you can add an enhancements. 
