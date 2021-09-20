# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 11:03:49 2020

@author: johns
"""

from os import listdir
from os.path import isfile, join
import shutil

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

path = 'ImagesToClassify'
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
        self.toggleWeather1 = ToggleButton(text = "Clear", group='weather', state='down')
        self.weatherLayout.add_widget(self.toggleWeather1)
        self.toggleWeather2 = ToggleButton(text = "Rain", group='weather')
        self.weatherLayout.add_widget(self.toggleWeather2)
        self.toggleWeather3 = ToggleButton(text = "Cloudy", group='weather')
        self.weatherLayout.add_widget(self.toggleWeather3)
        self.toggleWeather4 = ToggleButton(text = "Fog", group='weather')
        self.weatherLayout.add_widget(self.toggleWeather4)
        
        self.submitLabel = Label(text='Submit results for ' + images[i])
        self.buttonLayout.add_widget(self.submitLabel)
        self.buttonSubmit = Button(text='Submit')
        self.buttonSubmit.bind(on_press = self.pressed_buttonSubmit)
        self.buttonLayout.add_widget(self.buttonSubmit)
        
        # Image
        self.imageLayout = GridLayout(cols=1)
        self.mainLayout.add_widget(self.imageLayout)
        
        self.image = Image(source = 'ImagesToClassify/' + images[i] , allow_stretch = False, keep_ratio = True)
        self.imageLayout.add_widget(self.image)
        
    def pressed_buttonSubmit (self, instance):
        global i
        shutil.move('ImagesToClassify/' + images[i], 'ClassifiedImages/' + images[i])
    
        with open(logfile, "a", newline='') as fp:
            wr = csv.writer(fp, dialect = 'excel')
            wr.writerow((images[i], tog(self.toggleDay1.state),tog(self.toggleDay2.state),tog(self.toggleDay3.state),tog(self.toggleDay4.state),
                         tog(self.toggleWeather1.state),tog(self.toggleWeather2.state),tog(self.toggleWeather3.state),tog(self.toggleWeather4.state)))
                        
        i = i+1
        
        try:
            self.image.source = 'ImagesToClassify/' + images[i]
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
