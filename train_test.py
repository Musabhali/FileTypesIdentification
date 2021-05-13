# USAGE
# python filetypeidentifier.py --dir .\files\originalFilesForTesting

# import the necessary packages
from fileTypeIdentification.Feature_Extractor import LBP
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from imutils import paths
import argparse
import cv2
from glob import glob
import os, numpy as np, colorama
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore',category=DeprecationWarning)
from sklearn.metrics import classification_report, accuracy_score
import sklearn.model_selection as model_selection
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn import *
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix


#GLOBALS 
desc = LBP(36,9)
data = []
labels = []
c=100

model = svm.SVC(kernel='poly', degree=3, C=c) 


def identify():
    trainpath = r'.\files\training\*'
    testpath  =  r'.\files\testing'
    files_to_identify = r'.\files\scanned_files'


    for dirs in glob(trainpath):
        train_dataset_path = glob(dirs + '/*.png')
        for im in train_dataset_path:
            print(colorama.Fore.LIGHTGREEN_EX, f"[FileType Identifier] Training With : {im}")
            print(colorama.Style.RESET_ALL)
            img=cv2.imread(im)
            gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            fd = desc.describe(gray_image)
            data.append(fd)
            labels.append(im.split(os.path.sep)[-2])
            

    model.fit(data, labels)


    # loop over the testing images
    for test_dataset_path in paths.list_images(testpath):
        # load the image, convert it to grayscale, describe it,and classify it
        print(colorama.Fore.LIGHTBLUE_EX, f"[FileType Identifier] Testing With{test_dataset_path}")
        print(colorama.Style.RESET_ALL)
        # loads and read an image from path to file
        image = cv2.imread(test_dataset_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fd = desc.describe(gray_image)

        prediction = model.predict(fd.reshape(1, -1))[0]


    for scanned_files in paths.list_images(files_to_identify):
        #test_image= cv2.imread(r'D:\Project\images\testing\pdf6.pdf.png')
        #loads and read an image from path to file
        test_image = cv2.imread(scanned_files)
        #convert the color to grayscale 
        gray_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        feature = desc.describe(gray_image)
        prediction = model.predict(feature.reshape(1, -1))[0]
        #cv2.line(test_image,(15,25),(200,200),(0,),5)
        cv2.rectangle(test_image,(15,25),(100,150),(0,255,0), 5)
        cv2.putText(test_image, prediction[0], (20, 130), cv2.FONT_HERSHEY_SIMPLEX,
                            3.5, (200, 255, 255), 5, cv2.LINE_AA)
        # displays previous image 
        cv2.imshow('Test_image',test_image)
        # keeps the window open until a key is pressed
        cv2.waitKey(0)
        # clears all window buffers
        cv2.destroyAllWindows()


def report_gen():
    X_train, X_test, y_train, y_test = model_selection.train_test_split(data, labels, train_size=0.80, test_size=0.20, random_state=0)
    model.fit(X_train, y_train)
    poly_pred = model.predict(X_test)
    from sklearn.metrics import f1_score


    poly_accuracy = accuracy_score(y_test, poly_pred)
    poly_f1 = f1_score(y_test, poly_pred, average='weighted')
    print('Accuracy : ', "%.2f" % (poly_accuracy*100))
    print('F1 : ', "%.2f" % (poly_f1*100))


    #y_pred = model.predict(X_test)
    accuracy =accuracy_score(y_test, poly_pred)
    print(classification_report(y_test, poly_pred))
    print(colorama.Style.RESET_ALL)


    # Making the Confusion Matrix and plot confusion matrix

    cm = confusion_matrix(y_test, poly_pred)
    #cm/cm.astype(np.float).sum(axis=0)
    print(colorama.Fore.RED,model.classes_)
    print(colorama.Fore.LIGHTCYAN_EX,cm)
    print(colorama.Style.RESET_ALL)

    #plot confusion matrix

    plot_confusion_matrix(model, X_test, y_test)  
    plt.show()

   
# Normalise
# Plot non-normalized confusion matrix
    titles_options = [("Confusion matrix, without normalization", None),
                    ("Normalized confusion matrix", 'true')]
    for title, normalize in titles_options:
        disp = plot_confusion_matrix(model, X_test, y_test,
                                        display_labels=model.classes_,
                                        cmap=plt.cm.Greens,
                                        normalize=normalize)
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)

    plt.show()
    #python filetypeidentifier.py --dir .\Project\originalFilesForTesting