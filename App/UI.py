from tkinter import Button, Label, filedialog
from PIL import Image
from PIL.ImageTk import PhotoImage
import cv2
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.figure import Figure


class UI:
    def __init__(self, hwnd):
        self.Hwnd = hwnd
        self.ImageLabels = []
        self.Images = []
        self.OutputImage = Label(self.Hwnd)
        self.ImageCount = 0
        self.OpenImageBtn()
        self.SaveImageBtn()
        self.PrevImageBtn()
        self.NextImageBtn()

    def OpenImageBtn(self):
        Button(self.Hwnd, text="Open Image", 
        command=self.OpenImageFile).grid(row=0, column=0, columnspan=3, sticky="ew")
        
    def PrevImageBtn(self):
        Button(self.Hwnd, text="<<", 
        command=self.PrevImage).grid(row=1, column=0, sticky="ns")

    def NextImageBtn(self):
        Button(self.Hwnd, text=">>", 
        command=self.NextImage).grid(row=1, column=2, sticky="ns")

    def SaveImageBtn(self):
        Button(self.Hwnd, text="Save Image", 
        command=self.SaveImage).grid(row=2, column=0, columnspan=3, sticky="nsew")

    def OpenImageFile(self):
        filename = filedialog.askopenfilename(title="Open Image", filetypes=[("image file", (".jpg"))])

        if filename:

            if self.Images and self.ImageLabels:
                self.Images.clear()
                self.ImageLabels.clear()


            # Read Image
            image = cv2.imread(filename)

            # Resize Image
            image = cv2.resize(image, dsize=(512, 512), interpolation=cv2.INTER_NEAREST)
            
            # Initial mask
            facemask = np.zeros(image.shape[:2]).astype(np.uint8)
            mouthmask = np.zeros(image.shape[:2]).astype(np.uint8)
            
            # Load classifier
            faceCascade = cv2.CascadeClassifier("App/Model/Face.xml")
            mouthCascade = cv2.CascadeClassifier("App/Model/Mouth.xml")

            # Detect object from image with classifier
            faces = faceCascade.detectMultiScale(image, 1.3, 5)
            mouth = mouthCascade.detectMultiScale(image, 1.3, 5)

            # Mark object with rectangle
            for ((x0, y0, w0, h0), (x1, y1, w1, h1)) in zip(faces, mouth):
                cv2.rectangle(facemask, (x0, y0), (x0+w0, y0+h0), (255, 255, 255), -1)
                cv2.rectangle(mouthmask, (x1, y1), (x1+w1, y1+h1), (255, 255, 255), -1)

            


            colors = ['b', 'g', 'r']

            # Histogram
            fPltHisto = Figure()
            f = fPltHisto.add_subplot(221)
            m = fPltHisto.add_subplot(222)
            for i, color in enumerate(colors):
                f_hist_mask = cv2.calcHist([image],[i], facemask,[256],[0,256])
                f.plot(f_hist_mask, c=color)
                m_hist_mask = cv2.calcHist([image],[i], mouthmask,[256],[0,256])
                m.plot(m_hist_mask, c=color)
            
            f.title.set_text("Face Masked Histogram")
            m.title.set_text("Mouth Masked Histogram")

            # Save histogram to BytesIO
            faceimghisto = BytesIO()
            fPltHisto.savefig(faceimghisto)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Create Masked Image
            faceMaskedColor = cv2.bitwise_and(image, image, mask=facemask)
            mouthImMasked = cv2.bitwise_and(image, image, mask=mouthmask)

            # Convert image array to PIL Image
            image = Image.fromarray(image)
            facemask = Image.fromarray(facemask)
            mouthmask = Image.fromarray(mouthmask)
            faceMaskedColor = Image.fromarray(faceMaskedColor)
            mouthImMasked = Image.fromarray(mouthImMasked)
            fhisto = Image.open(faceimghisto).convert("RGB")

            # Add all PIL Image to list (Save file list)
            self.Images.append(image)
            self.Images.append(facemask)
            self.Images.append(mouthmask)
            self.Images.append(faceMaskedColor)
            self.Images.append(mouthImMasked)
            self.Images.append(fhisto)

            # Convert PIL Image to PhotoImage
            image = PhotoImage(image)
            facemask = PhotoImage(facemask)
            mouthmask = PhotoImage(mouthmask)
            faceMaskedColor = PhotoImage(faceMaskedColor)
            mouthImMasked = PhotoImage(mouthImMasked)
            fhisto = PhotoImage(fhisto)

            # Add all PhotoImage to list (Output Image)
            self.ImageLabels.append(image)
            self.ImageLabels.append(facemask)
            self.ImageLabels.append(mouthmask)
            self.ImageLabels.append(faceMaskedColor)
            self.ImageLabels.append(mouthImMasked)
            self.ImageLabels.append(fhisto)

            # Output Image with Label
            self.OutputImage = Label(image=self.ImageLabels[0])
            self.OutputImage.grid(row=1, column=1)

    def NextImage(self):
        if self.ImageLabels and self.ImageCount + 1 < len(self.ImageLabels):       
            self.ImageCount = self.ImageCount + 1
            self.OutputImage.grid_forget()
            self.OutputImage = Label(image=self.ImageLabels[self.ImageCount])
            self.OutputImage.grid(row=1, column=1)

    def PrevImage(self):
        if self.ImageLabels and self.ImageCount - 1 > -1:       
            self.ImageCount = self.ImageCount - 1
            self.OutputImage.grid_forget()
            self.OutputImage = Label(image=self.ImageLabels[self.ImageCount])
            self.OutputImage.grid(row=1, column=1)
    
    def SaveImage(self):
        if self.ImageLabels:
            filedirectory = filedialog.asksaveasfile(mode="w", defaultextension=".jpg")
            if not filedirectory:
                return
            self.Images[self.ImageCount].save(filedirectory)
            

