
from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder

Builder.load_string("""

<dictionary>:

   
    
    canvas.before:
      
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'data/kivy_main-08.jpg'
    

   
    BoxLayout:
        orientation: 'vertical'
       
        size_hint_y: None
        height: 50
        canvas.before:
            Color:
                rgba: (0, 0, 0, 1)
            Rectangle:
                size: self.size
                pos: self.pos
               
       
        Button:
            text: "BACK"
            bold:True
            font_size:20
            size_hint_y: 0.4
            background_color: (0,0,0, 1)
            background_normal: ''
            height: 40
            paddin:10
           
            font_size: 24
            on_press: root.disconnect4()
            
""")

class dictionary(Screen):
    def disconnect4(self):
        self.manager.transition = SlideTransition(direction="right")

        self.manager.current = 'home'