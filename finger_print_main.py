import tkinter as tk
import time
import sys
from pyfingerprint.pyfingerprint import PyFingerprint
import cv2
import tempfile
import numpy as np
import tkinter.filedialog
from PIL import ImageTk, Image
import os
from tkinter import W, E, N, S

path = "/tmp/fingerprint.bmp"

class UI(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.position = tk.StringVar()
        self.label1 = tk.Label(self, text="指紋鎖 Finger Print lock", fg='black', bg='white')
        # self.label1.grid(row=0, column=0)

        # Enroll button
        self.enroll = tk.Button(self, text="錄入 Enroll", command=self.enroll, background='black', fg='white')
        # self.enroll.grid(row=0, column=0)

        # Search button
        self.search = tk.Button(self, text="尋找匹配 Search", command=self.search, background='black', fg='white')
        # self.search.grid(row=0, column=1)

        # Delete button
        self.delete = tk.Button(self, text="刪除指紋 Delete", command=self.delete, background='black', fg='white')
        self.E1 = tk.Entry(self, textvariable=self.position, background='black', fg='white')

        self.label1.grid(row=0, columnspan=11, sticky=W+S+E+N, pady=5)
        self.enroll.grid(row=1, column=0, sticky=W+S+E+N)
        self.search.grid(row=1, column=1, sticky=W+S+E+N)
        self.delete.grid(row=1, column=2, sticky=W+S+E+N)
        self.E1.grid(row=1, column=3, sticky=W+S+E+N, columnspan=8)
        # output
        self.output = tk.Text(self, width=70, height=15, background='black', fg='white')
        self.output.grid(row=2, columnspan=4)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.output.yview)
        self.scrollbar.grid(row=2, column=10, sticky=N+S)
        self.output['yscrollcommand'] = self.scrollbar.set

        #display image
        #self.canvas = Canvas(self)
        #label = tk.Label(self)
        try:
            img = Image.open("fingerprint.bmp")
            label.img = ImageTk.PhotoImage(img)
            label['image'] = label.img
            label = tk.Label(self)
        except:
            pass
        #label.img = ImageTk.PhotoImage(img)
        
        # check if desktop has the fingerprint file
        #if os.path.isfile("fingerprint.bmp"):
        #    img = Image.open("fingerprint.bmp")
        #    label.img = ImageTk.PhotoImage(img)
        #    label['image'] = label.img
            #tk.update_idletasks()
        #else:

        #    img = Image.open("fingerprint.bmp")
        #    label.img = ImageTk.PhotoImage(img)
        #    label['image'] = label.img


        #label.pack()

        #self.img = ImageTk.Tk.PhotoImage(Image.open(path))
        #self.panel = tk.Label(self, image=self.img)
        #self.panel.pack(side = "bottom", fill="both", expand = "yes")


        self.configure(background='black')
        #self.pack()
        self.grid()

    def callback(self):
        label2 = tk.Label(self)
        #img2 = Image.open("fingerprint.bmp")
        #label.configure(image=img2)
        #label['image'] = label.img2


    def enroll(self):
        self.write('Initializing...' + '\n')
        print ('Initializing...')

        ##
        self.write('Preparing module...' + '\n')
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))

        ## Gets some sensor information
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
        self.write('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()) + '\n')

        ## Tries to enroll new finger
        try:
            self.write('Waiting for finger...' + '\n')
            ## Wait that finger is read
            while ( f.readImage() == False ):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(0x01)

            ## Checks if finger is already enrolled
            result = f.searchTemplate()
            positionNumber = result[0]

            if ( positionNumber >= 0 ):
                print('Template already exists at position #' + str(positionNumber))
                self.write('Template already exists at position #' + str(positionNumber) + '\n')

            print('Remove finger...')
            self.write('Remove finger...' + '\n')
            time.sleep(2)

            print('Waiting for same finger again...')
            self.write('Waiting for same finger again...' + '\n')
            ## Wait that finger is read again
            while ( f.readImage() == False ):
                pass

            print('Processing...')
            self.write('processing' + '\n')
            imageDestination =  '/home/pi/Desktop/fingerprint.bmp'
            f.downloadImage(imageDestination)

            ## Converts read image to characteristics and stores it in charbuffer 2
            f.convertImage(0x02)

            ## Compares the charbuffers
            if ( f.compareCharacteristics() == 0 ):
                raise Exception('Fingers do not match')

            ## Creates a template
            f.createTemplate()

            ## Saves template at new position number
            positionNumber = f.storeTemplate()
            print('Finger enrolled successfully!')
            self.write('Finger enrolled successfully!' + '\n')
            print('New template position #' + str(positionNumber))
            self.write('New template position #' + str(positionNumber) + '\n')

            img = cv2.imread(imageDestination,0)

            self.callback

            cv2.imshow('Image', img)
            cv2.waitKey(0)
            cv2.destroyWindow('Image')


        except Exception as e:
            print('Operation failed!')
            print('Exception message: ' + str(e))

        ##

    def search(self):
        self.write('Searching...' + '\n')
        print ('Searching...')
        ##
        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))

        ## Gets some sensor information
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
        self.write('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()) + '\n')
        ## Tries to search the finger and calculate hash
        try:
            print('Waiting for finger...')
            self.write('Waiting for finger...' + '\n')
            ## Wait that finger is read
            while ( f.readImage() == False ):
                pass

            print('Processing...')
            self.write('Processing' + '\n')

            imageDestination =  tempfile.gettempdir() + '/fingerprint.bmp'

            f.downloadImage(imageDestination)

            #print('The image was saved to "' + imageDestination + '".')

            ## Converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(0x01)

            ## Searchs template
            result = f.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]

            if ( positionNumber == -1 ):
                print('No match found!')
                self.write('No match found!' + '\n')
            else:
                print('Found template at position #' + str(positionNumber))
                self.write('Found template at position #' + str(positionNumber) + '\n')
                print('The accuracy score is: ' + str(accuracyScore))
                self.write('The accuracy score is: ' + str(accuracyScore) + '\n')

            img = cv2.imread(imageDestination,0)
            cv2.imshow('Image', img)
            cv2.waitKey(0)
            cv2.destroyWindow('Image')


            self.imshow('Image', img)
            self.waitkey(0)



        except Exception as e:
            print('Operation failed!')
            self.write('Operation failed!' + '\n')
            print('Exception message: ' + str(e))
            self.write('Exception message: ' + str(e) + '\n')

        ##
    def delete(self):

        try:
            f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

            if ( f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            self.write('The fingerprint sensor could not be initialized!' + str(e) + '\n')
            print('Exception message: ' + str(e))
            self.write('Exception message: ' + str(e) + '\n')


        ## Gets some sensor information
        print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
        self.write('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()) + '\n')

        ## Tries to delete the template of the finger
        try:
            #positionNumber = input('Please enter the template position you want to delete: ')
            positionNumber = self.position.get()
            positionNumber = int(positionNumber)

            if ( f.deleteTemplate(positionNumber) == True ):
                print('Template deleted!')
                self.write('Template deleted!' + '\n')
        except Exception as e:
            print('Operation failed!')
            self.write('Operation failed!' + '\n')
            print('Exception message: ' + str(e))
            self.write('Exception message: ' + str(e) + '\n')

    def write(self, txt):
        msg = str(txt)
        self.output.insert(tk.END,msg)
        self.update_idletasks()


if __name__ == '__main__':
    UI().mainloop()
