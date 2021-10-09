from os import listdir, mkdir
from os.path import isfile, join
import shutil

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

i = 0
folder = 'C:\Projects\Weather Detector\ImagesToClassify\\'
folder2 = 'C:\Projects\Weather Detector\ClassifiedImages\\'
images = [file for file in listdir(folder) if isfile(join(folder, file))]

class workoutWindow (BoxLayout):
    global folder
    global folder2
    global images
    global i

    path = StringProperty(folder + images[0])

    imageCount = StringProperty ("Image " + str(i+1) + " of " + str(len(images)) + " Images")
    aiGuess = StringProperty ("When AI is ready, AI guess will appear here")

    def submit (self, bt0, bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, bt9, bt10, bt11):
        global i
        global folder2
        val = 0

        if (bt0.state == "down"):
            val = 0
        elif (bt1.state == "down"):
            val = 1
        elif (bt2.state == "down"):
            val = 2
        elif (bt3.state == "down"):
            val = 3
        elif (bt4.state == "down"):
            val = 4
        elif (bt5.state == "down"):
            val = 5
        elif (bt6.state == "down"):
            val = 6
        elif (bt7.state == "down"):
            val = 7
        elif (bt8.state == "down"):
            val = 8
        elif (bt9.state == "down"):
            val = 9
        elif (bt10.state == "down"):
            val = 10
        elif (bt11.state == "down"):
            val = 11
        else:
            val = -1
        print (val)

        if (val >= 0):
            try:
                shutil.move(self.path, folder2 + "\\" + str(val) + "\\" + images[i])
            except:
                mkdir(folder2 + "\\" + str(val))
                shutil.move(self.path, folder2 + "\\" + str(val) + "\\" + images[i])

            i += 1
            self.imageCount = "Image " + str(i+1) + " of " + str(len(images)) + " Images"
            self.path = folder + images[i]

class labelerApp (App):
    pass

labelerApp().run()
