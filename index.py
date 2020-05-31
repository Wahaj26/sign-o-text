from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition,SlideTransition
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button



# from connected import Connected
from home import Home
from instructionBack import inc
from textBack import text
from voiceBack import voice
from disctionaryBack import dictionary

Builder.load_string("""
<Roots>:
    id: main_win
    orientation: "vertical"
    spacing: 10
    space_x: self.size[0]/3
    canvas.before:
        Color:
            rgba: (1, 1, 1,1)
        Rectangle:
            size: self.size
            pos: self.pos
            source:'data/kivy_main-01.jpg'
                
                   

    
    



   
     
        
    




    AnchorLayout:
      
        spacing: 10
        anchor_y:'bottom'
        Button:
            
            
            text: "START"
            font_size: 20
            bold: True
            size_hint_y: None
            size_hint_x: None
            height: 70
            width: 350
            background_normal: 'start_btn.png'
            border: 20,20,20,20
            on_press: root.start()
        Label:
            id: sp2
""")

class Roots(Screen):
  
    def start(self):
       
                #app = App.get_running_app()
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = 'home'
               # app.config.read(app.get_application_config())
                #app.config.write()

       

    
            
            


class SignOtextApp(App):
    def build(self):
        self.title = 'SIGN-O-TEXT'
        manager = ScreenManager()
        manager.add_widget(Roots(name='root'))
        manager.add_widget(Home(name='home'))
        manager.add_widget(inc(name='instruction'))
        manager.add_widget(text(name='signtext'))
        manager.add_widget(voice(name='signvoice'))
        manager.add_widget(dictionary(name='asldictionary'))
        
        return manager


if __name__=="__main__":
     SignOtextApp().run()
    