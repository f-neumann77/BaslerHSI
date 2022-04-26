import sys
from inter import *
from PyQt5 import QtCore, QtGui, QtWidgets
from pypylon import pylon
import cv2
import time
from time import sleep
#import RPi.GPIO as GPIO

class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
   
        self.ui.pushButton_4.clicked.connect(self.foto_)
        
        self.ui.pushButton_7.clicked.connect(self.res)

        self.ui.pushButton_5.clicked.connect(self.preview_)

    def preview_(self):
        STOP_ = True

        # conecting to the first available camera
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        # Grabing Continusely (video) with minimal delay
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

        while camera.IsGrabbing():
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
            # Access the image data
                image = converter.Convert(grabResult)
                img = image.GetArray()
                cv2.namedWindow('title', cv2.WINDOW_NORMAL)
                cv2.imshow('title', img)
                k = cv2.waitKey(1)
                print(k)
                if k == 27 or STOP_ == False:
                    break
            grabResult.Release()
    
        # Releasing the resource
        camera.StopGrabbing()

        cv2.destroyAllWindows()

    def stop_preview(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            STOP_ = False
        

    def foto_(self):

        try:

            NAME = str(self.ui.textEdit_6.toPlainText())
            dan = int(self.ui.textEdit.toPlainText())     # Kolichestvo shagov
            dan_2 = int(self.ui.textEdit_2.toPlainText()) # Napravlenie
            N = int(self.ui.textEdit_11.toPlainText())    #Rezim
            skor_ = float(self.ui.textEdit_12.toPlainText())      #Скорость(кол-во шагов в минуту)

            Exp_ = float(self.ui.textEdit_5.toPlainText())    #ZADAEM ExporsureTime
            k = dan
            
            pauza_ = 60.0 / skor_
            
            x = 1 # NOMER FOTO           
            j = 1 # schetchik foto
            i = 0 # schetchik shagov
            
            pin_3_YEL = 3     #STEP
            pin_14_BLUE = 14  #STRAHOVKA (ENA)
            pin_4_GREY = 4    #NAPRAVLENIE (DIR)
            pin_17_MS1 = 17   #                 №6 после земли ближе к процу
            pin_18_MS2 = 18   #REJIM oborota    №6 на 1 дальше чем предыдущи
            
            """
            GPIO.setmode(GPIO.BCM)      # ZADALI NOMERATIY PINOV
            
            GPIO.setup(pin_3_YEL, GPIO.OUT, initial = 1)    #step
            GPIO.setup(pin_14_BLUE, GPIO.OUT, initial = 1)  #strahowka (ENA)
            GPIO.setup(pin_4_GREY, GPIO.OUT, initial = 1)   #napravlenie step (DIR)
            GPIO.setup(pin_17_MS1, GPIO.OUT, initial = 0)
            GPIO.setup(pin_18_MS2, GPIO.OUT, initial = 0)
            
            if N == 1:
                GPIO.output(pin_17_MS1, 0)
                GPIO.output(pin_18_MS2, 0)
            elif N == 2:
                GPIO.output(pin_17_MS1, 1)
                GPIO.output(pin_18_MS2, 0)
            elif N == 4:
                GPIO.output(pin_17_MS1, 0)
                GPIO.output(pin_18_MS2, 1)
            else:
                GPIO.output(pin_17_MS1, 1)
                GPIO.output(pin_18_MS2, 1)
            
    

            GPIO.output(pin_4_GREY, dan_2)          #zadaem rejim raboti pinov  dan_2
            GPIO.output(pin_14_BLUE, 0)             #
            """
            img = pylon.PylonImage()
            tlf = pylon.TlFactory.GetInstance()

            cam = pylon.InstantCamera(tlf.CreateFirstDevice())
            cam.Open()
            cam.ExposureTime.SetValue(Exp_)
            cam.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)                                          

            for i in range(k):
                 with cam.RetrieveResult(9000) as result:
                    sleep(((pauza_)/2))
                    #GPIO.output(pin_3_YEL, 1)                    #
                    time.sleep(pauza_/2)                           #DELAEM SHAG
                                                     #
                    #GPIO.output(pin_3_YEL, 0)                    #
                    time.sleep(pauza_)
                    
                    print(i)                                     #
                
                    img.AttachGrabResultBuffer(result)

                    filename = (NAME+"_%d.png" % i)
                    img.Save(pylon.ImageFileFormat_Png, filename)   #DELAEM FOTO I SOHRANAYEM
                    img.Release()

                
            self.ui.textEdit_3.setText(str(j-1))
        finally:
            cam.StopGrabbing()
            cam.Close()
            #GPIO.cleanup()
            print("finish")
            
    def res(self):

        #GPIO.setmode(GPIO.BCM)

        #GPIO.cleanup()

        self.ui.textEdit.setText(str("")) 
        self.ui.textEdit_2.setText(str("")) 
        self.ui.textEdit_3.setText(str("")) 
        self.ui.textEdit_5.setText(str("")) 
        self.ui.textEdit_6.setText(str("")) 
        self.ui.textEdit_8.setText(str("")) 
        self.ui.textEdit_11.setText(str(""))
        self.ui.textEdit_12.setText(str(""))
        
        print("restart")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
