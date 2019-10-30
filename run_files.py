path = r'C:\Users\josed\Desktop\Reprovado'

import text_detection_app as ap
import os
#files = []
file_list = os.listdir(path)
imgs = [arq for arq in file_list if arq.lower().endswith((".jpg", ".jpeg", ".png"))]
print("[INFO] Found {} images at {}".format(len(imgs), path))
for f in imgs:
    ap.args['image']=(path+'/'+f)
    ap.load()
print("[INFO] All process finished")
