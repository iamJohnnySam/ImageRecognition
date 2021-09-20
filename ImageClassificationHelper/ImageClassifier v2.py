from os import listdir
from os.path import isfile, join
import shutil

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
        
        self.group = Label(text='Select Workout')
        self.buttonLayout.add_widget(self.group)
        

        self.ButLayout = GridLayout(cols=4)
        self.buttonLayout.add_widget(self.ButLayout)

        self.toggleAction1 = ToggleButton(text = "Vacant", group='classify', state='down')
        self.ButLayout.add_widget(self.toggleAction1)
        self.toggleAction2 = ToggleButton(text = "Idle", group='classify')
        self.ButLayout.add_widget(self.toggleAction2)
        self.toggleAction3 = ToggleButton(text = "Crunches", group='classify')
        self.ButLayout.add_widget(self.toggleAction3)
        self.toggleAction4 = ToggleButton(text = "Elliptical", group='classify')
        self.ButLayout.add_widget(self.toggleAction4)
        self.toggleAction5 = ToggleButton(text = "Deadlifts", group='classify')
        self.ButLayout.add_widget(self.toggleAction5)
        self.toggleAction6 = ToggleButton(text = "Squats", group='classify')
        self.ButLayout.add_widget(self.toggleAction6)
        self.toggleAction7 = ToggleButton(text = "Fly", group='classify')
        self.ButLayout.add_widget(self.toggleAction7)
        self.toggleAction8 = ToggleButton(text = "Benches", group='classify')
        self.ButLayout.add_widget(self.toggleAction8)
        self.toggleAction9 = ToggleButton(text = "Bullworker", group='classify')
        self.ButLayout.add_widget(self.toggleAction9)
        self.toggleAction10 = ToggleButton(text = "Pushups", group='classify')
        self.ButLayout.add_widget(self.toggleAction10)
        self.toggleAction11 = ToggleButton(text = "Stretching", group='classify')
        self.ButLayout.add_widget(self.toggleAction11)
        self.toggleAction12 = ToggleButton(text = "N/A", group='classify')
        self.ButLayout.add_widget(self.toggleAction12)
        
        self.submitLabel = Label(text='Submit results for ' + images[i])
        self.buttonLayout.add_widget(self.submitLabel)
        self.buttonSubmit = Button(text='Submit')
        self.buttonSubmit.bind(on_press = self.pressed_buttonSubmit)
        self.buttonLayout.add_widget(self.buttonSubmit)
        
        # Image
        self.imageLayout = GridLayout(cols=1)
        self.mainLayout.add_widget(self.imageLayout)
        
        self.image = Image(source = path + images[i] , allow_stretch = False, keep_ratio = True)
        self.imageLayout.add_widget(self.image)
        
    def pressed_buttonSubmit (self, instance):
        global i
        folder = 0
        if tog(self.toggleAction1.state):
            folder = 0
        elif tog(self.toggleAction2.state):
            folder = 1
        elif tog(self.toggleAction3.state):
            folder = 2
        elif tog(self.toggleAction4.state):
            folder = 3
        elif tog(self.toggleAction5.state):
            folder = 4
        elif tog(self.toggleAction6.state):
            folder = 5
        elif tog(self.toggleAction7.state):
            folder = 6
        elif tog(self.toggleAction8.state):
            folder = 7
        elif tog(self.toggleAction9.state):
            folder = 8
        elif tog(self.toggleAction10.state):
            folder = 9
        elif tog(self.toggleAction11.state):
            folder = 10
        elif tog(self.toggleAction12.state):
            folder = 11
        shutil.move(path + images[i], path2 + str(folder) + "\\" + images[i])

        i = i+1
        
        try:
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
