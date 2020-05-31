
from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
import kivy.core.text
import cv2
from kivy.base import EventLoop
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import cv2, pickle
import numpy as np
import tensorflow as tf
import os
import sqlite3, pyttsx3
from keras.models import load_model
from threading import Thread
from kivy.properties import StringProperty
from kivy.clock import Clock

engine = pyttsx3.init()
engine.setProperty('rate', 150)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
model = load_model('cnn_model_keras2.h5')

text = " "
word = " "
count_same_frame = 0
threshold = ""


def get_hand_hist():
    with open("hist", "rb") as f:
        hist = pickle.load(f)
    return hist

def get_image_size():
    img = cv2.imread('1.jpg', 0)
    return img.shape

image_x, image_y = get_image_size()

def keras_process_image(img):
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (1, image_x, image_y, 1))
    return img

def keras_predict(model, image):
    processed = keras_process_image(image)
    pred_probab = model.predict(processed)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class

def get_pred_text_from_db(pred_class):
    conn = sqlite3.connect("gesture_db.db")
    cmd = "SELECT g_name FROM gesture WHERE g_id="+str(pred_class)
    cursor = conn.execute(cmd)
    for row in cursor:
        return row[0]

def get_pred_from_contour(contour, thresh):
    x1, y1, w1, h1 = cv2.boundingRect(contour)
    save_img = thresh[y1:y1+h1, x1:x1+w1]
    text = ""
    if w1 > h1:
        save_img = cv2.copyMakeBorder(save_img, int((w1-h1)/2) , int((w1-h1)/2) , 0, 0, cv2.BORDER_CONSTANT, (0, 0, 0))
    elif h1 > w1:
        save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1-w1)/2) , int((h1-w1)/2) , cv2.BORDER_CONSTANT, (0, 0, 0))
    pred_probab, pred_class = keras_predict(model, save_img)
    if pred_probab*100 > 70:
        text = get_pred_text_from_db(pred_class)
    return text

x, y, w, h = 300, 100, 300, 300
is_voice_on = True

def get_img_contour_thresh(img):
    lower_thresh1 = 129 
    upper_thresh1 = 255
    img = cv2.flip(img,1)
    crop_img = img[70:300, 70:300]
    crop_img_2 = img[70:300, 70:300]
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  
    lower_red = np.array([110,50,50])
    upper_red = np.array([130,255,255])            
    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(img,img, mask= mask)
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)
    _ ,newthresh = cv2.threshold(blurred, lower_thresh1, upper_thresh1, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours = cv2.findContours(newthresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
    return img, contours, newthresh

def say_text(text):
    if not is_voice_on:
        return
    while engine._inLoop:
        pass
    engine.say(text)
    engine.runAndWait()


class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = None

    def start(self, capture, fps=30):
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.capture = None

    def update(self, dt):
        global text,word ,count_same_frame,threshold
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, -1)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
            img, contours, thresh = get_img_contour_thresh(frame)
            old_text = text
            if len(contours) > 0:
                contour = max(contours, key = cv2.contourArea)
                if cv2.contourArea(contour) > 10000:
                    text = get_pred_from_contour(contour, thresh)
                    if old_text == text:
                        count_same_frame += 1
                    else:
                        count_same_frame = 0
                    if count_same_frame > 20:
                        if len(text) == 1:
                            Thread(target=say_text, args=(text, )).start()
                        word = word + text
                        count_same_frame = 0
                elif cv2.contourArea(contour) < 1000:
                    if word != '':
                        Thread(target=say_text, args=(word, )).start()
                    text = ""
                    word = ""
            else:
                if word != '':
                    Thread(target=say_text, args=(word, )).start()
                text = ""
                word = ""
            threshold = thresh

capture = None


class Threshold(Image):
    def __init__(self, **kwargs):
        super(Threshold, self).__init__(**kwargs)
        self.capture = None

    def start(self, capture, fps=30):
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.capture = None

    def update(self, dt):
        global text,word ,count_same_frame,threshold
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            b = cv2.flip(threshold,0)
            buf = b.tostring()
            image_texture = Texture.create(
                size=(threshold.shape[1], threshold.shape[0]), colorfmt='luminance')
            image_texture.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture



Builder.load_string("""
<voice>:

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
            source:'data/kivy_main-07.jpg'
   
        
    BoxLayout:
        orientation: "vertical"
       

        Label:
            height: 50
            size_hint_y: None
            
            color:1,1,1,1
            font_size:'40dp'
           
            
            bold: True
        
        
        KivyCamera:
            id: qrcam 
            size: root.width, root.height



        

       
          
        BoxLayout:
            orientation:"horizontal"
            size: root.width, root.height
            Threshold:
                id:qrthreshold
                size_hint: 0.5,0.8
                pos:(0,0)

            Button:
                id: butt_start1
                size_hint: 0.3,0.8
                text: root.my
                on_press: root.dostart()
            
       
            Button:
                id: butt_start1
                size_hint: 0.8,0.8
                text: root.words
                on_press: root.dostart()
               
               
        BoxLayout:
            size_hint: None, None
            size: root.width, 26
            spacing: 20
            pos: (0,70)

            Button:
                id: butt_start1
                text: "Back"
                background_normal: 'start_btn.png'
                on_press: root.back()
            
            Button:
                id: butt_start1
                text: "Start"
                background_normal: 'start_btn.png'
                on_press: root.dostart()

            Button:
                id: butt_exit
                text: "Exist"
                background_normal: 'start_btn.png'
                on_press: root.doexit()
""")

class voice(Screen):
    global text,word ,count_same_frame,threshold
    my = StringProperty("wahaj")
    words = StringProperty("none")

    def back(self):
        global capture
        if capture != None:
            capture.release()
            capture = None
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'home'


    def init_qrtest(self):
        pass

    def dostart(self, *largs):
        global capture
        capture = cv2.VideoCapture(0)
        self.ids.qrcam.start(capture)
        self.ids.qrthreshold.start(capture)
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        
    def doexit(self):
        global capture
        if capture != None:
            capture.release()
            capture = None
        EventLoop.close()


    def update(self, dt):
        self.my = text
        self.words = word