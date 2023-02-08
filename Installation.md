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





