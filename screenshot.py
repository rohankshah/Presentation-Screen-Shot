# Take screenshot
import pyscreenshot as ImageGrab

# Compare similar
from PIL import Image
import imagehash

# For schedule
import schedule

from threading import Timer
import time
import math
import os

def getFileName():
    fileName = math.ceil(time.time())
    return str(fileName) + ".png"

def clickPic():
    im = ImageGrab.grab(bbox=(14, 160, 1027, 730))  # X1,Y1,X2,Y2
    fileName = "./pics/" + getFileName() 
    im.save(fileName)

def checkSimilar(pic1, pic2):
    first = imagehash.average_hash(Image.open(pic1))
    second = imagehash.average_hash(Image.open(pic2))
    cutoff = 5
    if first - second < cutoff:
        return True
    else:
        return False

def newest(path):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)

def getNewest(dirpath):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a

def job():
    clickPic()    
    li = getNewest("./pics")
    li.remove('.DS_Store')
    if (len(li) == 1):
        print('First')
        return
    lastPic = "./pics/" + li[-1]
    prevPic = "./pics/" + li[-2]
    if (checkSimilar(lastPic, prevPic)):
        print('Same')
        os.remove(lastPic)
    else:
        print('New')
        
schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)






