from os import listdir
from os.path import isfile, join
import shutil
from PIL import Image

import csv
logfile = "Output.csv"

# Import Kivy Libraries
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.image import Image

path = 'C:\Projects\Weather Detector\ImagesToClassify\\'
path2 = 'C:\Projects\Weather Detector\ClassifiedImages\\'
images = [file for file in listdir(path) if isfile(join(path, file))]

global i
i = 0

def tog (temp):
    temp = str(temp)
    if temp == 'down':
        return 1
    else:
        return 0


class screenMain(FloatLayout):    
    def __init__ (self, **kwargs):
        super(screenMain, self).__init__(**kwargs)
        
        self.mainLayout = GridLayout(cols=2)        
        self.add_widget(self.mainLayout)
        
        #Buttons
        self.buttonLayout = GridLayout(cols=1)
        self.mainLayout.add_widget(self.buttonLayout)
        
        self.group1 = Label(text='Time of Day')
        self.buttonLayout.add_widget(self.group1)
        
        self.dayLayout = GridLayout(cols=4)
        self.buttonLayout.add_widget(self.dayLayout)
        self.toggleDay1 = ToggleButton(text = "Morning", group='day', state='down')
        self.dayLayout.add_widget(self.toggleDay1)
        self.toggleDay2 = ToggleButton(text = "Afternoon", group='day')
        self.dayLayout.add_widget(self.toggleDay2)
        self.toggleDay3 = ToggleButton(text = "Dusk", group='day')
        self.dayLayout.add_widget(self.toggleDay3)
        self.toggleDay4 = ToggleButton(text = "Night", group='day')
        self.dayLayout.add_widget(self.toggleDay4)
        
        self.group2 = Label(text='Weather')
        self.buttonLayout.add_widget(self.group2)
        
        self.weatherLayout = GridLayout(cols=4)
        self.buttonLayout.add_widget(self.weatherLayout)
        self.toggleWeather1 = ToggleButton(text = "Usual", group='classify', state='down')
        self.weatherLayout.add_widget(self.toggleWeather1)
        self.toggleWeather2 = ToggleButton(text = "Unusual", group='classify')
        self.weatherLayout.add_widget(self.toggleWeather2)
        #self.toggleWeather3 = ToggleButton(text = "Cloudy", group='classify')
        #self.weatherLayout.add_widget(self.toggleWeather3)
        #self.toggleWeather4 = ToggleButton(text = "Fog", group='classify')
        #self.weatherLayout.add_widget(self.toggleWeather4)
        
        self.submitLabel = Label(text='Submit results for ' + images[i])
        self.buttonLayout.add_widget(self.submitLabel)
        self.buttonSubmit = Button(text='Submit')
        self.buttonSubmit.bind(on_press = self.pressed_buttonSubmit)
        self.buttonLayout.add_widget(self.buttonSubmit)
        
        # Image
        self.imageLayout = GridLayout(cols=1)
        self.mainLayout.add_widget(self.imageLayout)
        
        im = Image.open(path + images[i])
        im = im.rotate(270, expand=True)
        im.save (path + images[i])
        self.image = Image(source = path + images[i] , allow_stretch = False, keep_ratio = True)
        self.imageLayout.add_widget(self.image)
        
    def pressed_buttonSubmit (self, instance):
        global i
        folder = 0
        if tog(self.toggleWeather1.state):
            folder = 0
        elif tog(self.toggleWeather2.state):
            folder = 1
        shutil.move(path + images[i], path2 + folder + "\\" + images[i])
    
        with open(logfile, "a", newline='') as fp:
            wr = csv.writer(fp, dialect = 'excel')
            wr.writerow((images[i], tog(self.toggleDay1.state),tog(self.toggleDay2.state),tog(self.toggleDay3.state),tog(self.toggleDay4.state),
                         tog(self.toggleWeather1.state),tog(self.toggleWeather2.state),tog(self.toggleWeather3.state),tog(self.toggleWeather4.state)))
                        
        i = i+1
        
        try:
            im = Image.open(path + images[i])
            im = im.rotate(270, expand=True)
            im.save (path + images[i])
            self.image.source = path + images[i]
            self.submitLabel.text = 'Submit results for ' + images[i]
        except:
            print("End")
            App.get_running_app().stop()
        
# Main
class ImageClassifier(App):
    def build(self):
        GUI = screenMain()
        return GUI
    
if __name__ == "__main__":
    ImageClassifier().run()
