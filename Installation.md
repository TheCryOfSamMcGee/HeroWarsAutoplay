## Installation instructions

### How to get a python IDE. 

Download link: [https://www.python.org/downloads/](https://www.python.org/downloads/)
Details on python IDEs: [https://realpython.com/python-idle/](https://realpython.com/python-idle/)

##Quick code for installing everything else

Once you have python installed on your system, open up 'command prompt' (you can open it by searching for it in Windows.) In that little screen, copy+paste or type the following commands.
These will install the python packages that that the script needs to run. 

        pip install numpy
        pip install ctypes
        pip install mss
        pip intall PILLOW 
        pip install opencv-python
        pip install pywin32
        pip install scikit-image
        pip install pyautogui
        pip install pytesseract 
        
        
## Setting up the script

Download the script called 'V3_Autoplay.py' and open it up from the python IDLE interface. From there, edit the following to match your computer. 

First, make sure you tell the script where you have the script saved. You should see this line of code Change this line of code so that it points to the folder that you have the python script saved it. If you saved the python script in your Documents folder, you can just remove the \\FBPython from the link, and change the username to whatever your username is. As for the pytesseract link, you just need to find the folder that Tessearct-OCR is installed in. Usually, it should just be Program Files, but sometimes it may be installed in Program Files (86x). 

                
                #################################################################

                ###############  Code set up secttion

                ################################################################
                
                #### set your own directory
                os.chdir('C:\\Users\\JohnDoe\\Documents\\FBPython')
                
                ## example: Your PC username is MarkAnthony, and you saved the script directly in the Documents folder. So you need to change the script to say
                # os.chdir('C:\\Users\\MarkAnthony\\Documents')

                ####Path to tesseract installation folder.
                pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


The last variable you can set allows you to slow down the script to deal with lag on loading speeds. If you have a slower internet, set the variable setLoadTime to a higher value. If you have a faster internet, then set it lower. The number represent the number of seconds the script will wait when going to and from the Guild page, and twice the amount of time it'll wait when going to the Tower. 

                #This variable is the number of seconds that the program should wait when switching locations within Hero wars. This is important because slower internets can slow down the load times, and mess up the script. 
                setLoadtime = 10
                ## Right now, it's set to 10 seconds. I have fast internet (200 mbps), but for some reason Hero Wars will run slow sometimes, so I set it to 10 seconds to avoid any issues. 
                
With this, you should have the script ready to run. Just go to the 'Run' table in python IDLE and click 'Run Module'. It should open a new window, called a python shell, where the function will run. 


## More details

### Pytessearct, scikit-image, etc...


The above packages allows python to interface with windows, move the mouse, and read text of your screen. 

Pytesseract in particular allows you to use Google text AI to identify text on your screen and read it - allowing the script to read some of the buttons. 
Unfortunately, I haven't been able to get it to work for all the text locations, just buttons. 

Pytessearct: [https://pypi.org/project/pytesseract/](https://pypi.org/project/pytesseract/)
Scikit-learn: [https://scikit-learn.org/stable/index.html](https://scikit-learn.org/stable/index.html)
OpenCV-Python: [https://pypi.org/project/opencv-python/](https://pypi.org/project/opencv-python/)
Python PILLOW: [https://python-pillow.org/](https://python-pillow.org/)

### Side note:

This code was initially inspired by this article: [https://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117](https://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117)

The initial bits were modified from there, and I added many additional layers, including image recognition. 





