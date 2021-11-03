import os
from posixpath import join
from tkinter import Button, Label, filedialog
from PIL import Image, ImageOps
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
        self.ImageCount = 0
        self.MaxSize = (720, 720)
        self.PhotoPrevBtn = PhotoImage(file="App/Assets/previous.png")
        Button(self.Hwnd, image=self.PhotoPrevBtn, border=0, command=self.PrevImage).grid(row=0, column=0, sticky="nsw")

        self.OutputImage = Label(self.Hwnd)
        self.OutputImage.grid(row=0, column=1, padx=15, pady=15)

        self.PhotoNextBtn = PhotoImage(file="App/Assets/next.png")
        Button(self.Hwnd, image=self.PhotoNextBtn, border=0, command=self.NextImage).grid(row=0, column=2, sticky="nse")
        
    def SetImage(self, filepath):
        if os.path.exists(os.path.join(os.getcwd(), "thumbnail.png")):
            os.remove("thumbnail.png")

        if self.Images and self.ImageLabels:
            self.Images.clear()
            self.ImageLabels.clear()
        
        original = Image.open(filepath)
        original = ImageOps.exif_transpose(original)
        original.thumbnail(self.MaxSize, Image.ANTIALIAS)
        original.save("thumbnail.png")

        # Read Image
        image = cv2.imread("thumbnail.png")

            
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

        

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Create Masked Image
        faceMaskedColor = cv2.bitwise_and(image, image, mask=facemask)
        mouthMaskedColor = cv2.bitwise_and(image, image, mask=mouthmask)

        # Create Gray Image
        faceMaskedGray = cv2.cvtColor(faceMaskedColor, cv2.COLOR_BGR2GRAY)
        mouthMaskedGray = cv2.cvtColor(mouthMaskedColor, cv2.COLOR_BGR2GRAY)

        # Threshold
        ret, faceth = cv2.threshold(faceMaskedGray, 200, 255, cv2.THRESH_BINARY_INV)
        
        faceunion = cv2.bitwise_and(facemask, faceth)
        face = cv2.bitwise_and(image, image, mask=faceunion)

        # Histogram
        fPltHisto = Figure()
        f = fPltHisto.add_subplot(221)
        m = fPltHisto.add_subplot(222)
        for i, color in enumerate(colors):
            f_hist_mask = cv2.calcHist([face],[i], facemask, [256],[0,256])
            f.plot(f_hist_mask, c=color)
            m_hist_mask = cv2.calcHist([image],[i], mouthmask,[256],[0,256])
            m.plot(m_hist_mask, c=color)
            
        f.title.set_text("Face Histogram")
        m.title.set_text("Mouth Histogram")

        # Save histogram to BytesIO
        faceimghisto = BytesIO()
        fPltHisto.savefig(faceimghisto)


        # Convert image array to PIL Image
        image = Image.fromarray(image)
        facemask = Image.fromarray(facemask)
        mouthmask = Image.fromarray(mouthmask)
        faceMaskedColor = Image.fromarray(faceMaskedColor)
        mouthMaskedColor = Image.fromarray(mouthMaskedColor)
        faceMaskedGray = Image.fromarray(faceMaskedGray)
        mouthMaskedGray = Image.fromarray(mouthMaskedGray)
        faceth = Image.fromarray(faceth)
        faceunion = Image.fromarray(faceunion)
        face = Image.fromarray(face)
        fhisto = Image.open(faceimghisto).convert("RGB")

        # Add all PIL Image to list (Save file list)
        self.Images.append(image)
        self.Images.append(facemask)
        self.Images.append(mouthmask)
        self.Images.append(faceMaskedColor)
        self.Images.append(mouthMaskedColor)
        self.Images.append(faceMaskedGray)
        self.Images.append(mouthMaskedGray)
        self.Images.append(faceth)
        self.Images.append(faceunion)
        self.Images.append(face)
        self.Images.append(fhisto)

        # Convert PIL Image to PhotoImage
        image = PhotoImage(image)
        facemask = PhotoImage(facemask)
        mouthmask = PhotoImage(mouthmask)
        faceMaskedColor = PhotoImage(faceMaskedColor)
        mouthMaskedColor = PhotoImage(mouthMaskedColor)
        faceMaskedGray = PhotoImage(faceMaskedGray)
        mouthMaskedGray = PhotoImage(mouthMaskedGray)
        faceth = PhotoImage(faceth)
        faceunion = PhotoImage(faceunion)
        face = PhotoImage(face)
        fhisto = PhotoImage(fhisto)

        # Add all PhotoImage to list (Output Image)
        self.ImageLabels.append(image)
        self.ImageLabels.append(facemask)
        self.ImageLabels.append(mouthmask)
        self.ImageLabels.append(faceMaskedColor)
        self.ImageLabels.append(mouthMaskedColor)
        self.ImageLabels.append(faceMaskedGray)
        self.ImageLabels.append(mouthMaskedGray)
        self.ImageLabels.append(faceth)
        self.ImageLabels.append(faceunion)
        self.ImageLabels.append(face)
        self.ImageLabels.append(fhisto)

        # Output Image with Label
        self.OutputImage.configure(image=self.ImageLabels[0])
        self.OutputImage.ImageTk = self.ImageLabels[0]
            

    def NextImage(self):
        if self.ImageLabels and self.ImageCount + 1 < len(self.ImageLabels):       
            self.ImageCount = self.ImageCount + 1
            self.OutputImage.grid_forget()
            self.OutputImage.configure(image=self.ImageLabels[self.ImageCount])
            self.OutputImage.ImageTk = self.ImageLabels[self.ImageCount]
            self.OutputImage.grid(row=0, column=1, padx=15, pady=15)

    def PrevImage(self):
        if self.ImageLabels and self.ImageCount - 1 > -1:       
            self.ImageCount = self.ImageCount - 1
            self.OutputImage.grid_forget()
            self.OutputImage.configure(image=self.ImageLabels[self.ImageCount])
            self.OutputImage.ImageTk = self.ImageLabels[self.ImageCount]
            self.OutputImage.grid(row=0, column=1, padx=15, pady=15)
    
    def SaveImage(self):
        if self.ImageLabels:
            filedirectory = filedialog.asksaveasfile(mode="w", defaultextension=".jpg")
            if not filedirectory:
                return
            self.Images[self.ImageCount].save(filedirectory)
            

