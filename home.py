
from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder

Builder.load_string("""
<Home>:

   
    
    canvas.before:
      
        Rectangle:
            size: self.size
            pos: self.pos
            source: 'data/kivy_main-02.jpg'
    AnchorLayout:
        size_hint: None, None
        size: 50, 50
        pos:(0,500)
        anchor_x:'center'
        anchor_y:'center'
        Button:
            text:"Back"
            font_size: 20
            bold: True
            background_normal: 'start_btn.png'
            border: 20,20,20,20
        


    BoxLayout:
        size_hint: None, None
        size: root.width, 70
        spacing: 20
        pos: (0,70)

        Button:
            text:"Instruction"
            font_size: 20
            bold: True
            background_normal: 'start_btn.png'
            border: 20,20,20,20
            on_press: root.instructions()
        Button:
            text:"Sign-Text-Word"
            font_size: 20
            bold: True
            background_normal: 'start_btn.png'
            border: 20,20,20,20
            on_press: root.signtextWords()
        Button:
            text:"Sign-Text-Letter"
            font_size: 20
            bold: True
            background_normal: 'start_btn.png'
            border: 20,20,20,20
            on_press: root.signtextLetters()
        Button:
            text:"ASL Dictionary"
            font_size: 20
            bold: True
            background_normal: 'start_btn.png'
            border: 20,20,20,20
            on_press: root.asldictionary()

       



      
          
    
   
        





""")



class Home(Screen):
    def back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'root'

    def instructions(self):
      #  app = App.get_running_app()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'instruction'
       # app.config.write()
    
    def signtextWords(self):
   #     app = App.get_running_app()
               # app.username = loginText
                #app.password = passwordText
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'signtext'
               # app.config.read(app.get_application_config())
    #    app.config.write()
    

    def signtextLetters(self):
    #    app = App.get_running_app()
               # app.username = loginText
                #app.password = passwordText
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'signvoice'
               # app.config.read(app.get_application_config())
     #   app.config.write()
    

    def asldictionary(self):
     #   app = App.get_running_app()
               # app.username = loginText
                #app.password = passwordText
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'asldictionary'
               # app.config.read(app.get_application_config())
      #  app.config.write()


 
