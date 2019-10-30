# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)
from PIL import Image as pi
from PIL import ImageFilter
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
import os

 
import cv2
import numpy as np
import time
import text_detection_app as tda


class camera_activity(App):
    def build(self):
        e = CameraClick()
        Clock.schedule_interval(e.iniciar, 0.02)  

        return e

class CameraClick(BoxLayout):
    cap = cv2.VideoCapture(0)
    cap.read()
    CODIGO = 'fitec'
    item = 'PLACA' 
    texto=''
    img=None
    texture1=None
    at =True
    
    def atualizaImagem(self, dt):
        try:
            if (self.texto.lower().rfind(self.CODIGO.lower())!=-1):
                self.ids.label.text = '\t TEXTO '+self.CODIGO.upper()+' ENCONTRADO!'
                self.ids.img.texture = self.texture1
                self.ids.box.disabled = False
                self.ids.box.opacity = 100
            else:
                ret, frame = self.cap.read()
                self.ids.label.text = 'Procurando'
                if ret:
                    self.img,self.texto = tda.load(frame)
                    self.ids.box.disabled = True
                    self.ids.box.opacity = 0
                    self.ids.label.text += '.'
                    buf1 = cv2.flip(self.img, 0)
                    buf = buf1.tostring()
                    self.texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                    self.texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                    self.ids.img.texture = self.texture1
                    ## Preparação prar aplicar novos filtros
                    #m2 = pi.open('images/placa.jpg')
                    #m2 = m2.filter(ImageFilter.SHARPEN) 
                    #m2.save('placa2.jpg')           
        except:
            print("[ERRO] Capture error")                            
            self.ids.label.text += '...'
            time.sleep(0.5)

    def iniciar(self,lixo):
        if self.at:
            if(len(self.ids.label.text)<120):
                self.ids.label.text += '|'
            else:
                self.ids.label.text = 'Pronto!'
                self.at=False
                Clock.schedule_interval(self.atualizaImagem, 0.01)   
        
    def save(self):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        if not os.path.exists('captures'):
            os.mkdir('captures')
        cv2.imwrite("captures/{}-{}_{}.jpg".format(self.item,self.CODIGO,timestr),self.img)
        self.texto = ''

    def repeat(self):
        self.texto = ''

camera_activity().run()