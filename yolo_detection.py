import cv2
import os
import torch
from PIL import Image
from io import BytesIO


# global variables 

# strings at index 0 is not used, it
# is to make array indexing simple
one = [ "", "one ", "two ", "three ", "four ",
        "five ", "six ", "seven ", "eight ",
        "nine ", "ten ", "eleven ", "twelve ",
        "thirteen ", "fourteen ", "fifteen ",
        "sixteen ", "seventeen ", "eighteen ",
        "nineteen "];
 
# strings at index 0 and 1 are not used,
# they is to make array indexing simple
ten = [ "", "", "twenty ", "thirty ", "forty ",
        "fifty ", "sixty ", "seventy ", "eighty ",
        "ninety "];

class CurrencyNotesDetection:
    """
    Class implements Yolo5 model to make inferences on a source provided/youtube video using Opencv2.
    """

    def __init__(self, model_name):
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        :param out_file: A valid output file name.
        """
        self.model = self.load_model(model_name)
        # similar to coco.names contains ['10Rupees','20Rupees',...]
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)

    def load_model(self, model_name):
        """
        Loads Yolo5 model from pytorch hub.
        :return: Customed Trained Pytorch model.
        """
        # Custom Model
        # model = torch.hub.load('ultralytics/yolov5', 'custom', path='path/to/best.pt',force_reload=True)  # default
        # model = torch.hub.load('ultralytics/yolov5','custom', path=model_name, force_reload=True, device='cpu')
        # model = torch.hub.load('/home/gowtham/MajorProject/yolov5_custom/yolov5', 'custom', path=model_name, source='local')  # local repo
        model = torch.hub.load('./yolov5', 'custom', path=model_name, source='local')  # local repo
        
        # Yolo Model from Web
        # for file/URI/PIL/cv2/np inputs and NMS
        # model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

        return model

    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]

    def numToWords(self,n, s):
 
        str = ""
        
        # if n is more than 19, divide it
        if (n > 19):
            str += ten[n // 10] + one[n % 10]
        else:
            str += one[n]
    
        # if n is non-zero
        if(n != 0):
            str += s
    
        return str

    def convertToWords(self,n):
        # stores word representation of given
        # number n
        out = ""

        # handles digits at ten millions and
        # hundred millions places (if any)
        out += self.numToWords((n // 10000000),"crore ")

        # handles digits at hundred thousands
        # and one millions places (if any)
        out += self.numToWords(((n // 100000) % 100),"lakh ")

        # handles digits at thousands and tens
        # thousands places (if any)
        out += self.numToWords(((n // 1000) % 100),"thousand ")

        # handles digit at hundreds places (if any)
        out += self.numToWords(((n // 100) % 10),"hundred ")

        if (n > 100 and n % 100):
            out += "and "

        # handles digits at ones and tens
        # places (if any)
        out += self.numToWords((n % 100), "")

        return out

    def get_text(self,labelCnt):
        text = "Image contains"
        noOfLabels,counter = len(labelCnt),0
        for k,v in labelCnt.items():
            text += " {}{} {} ".format(self.convertToWords(v),k,"Notes" if v>1 else "Note")
            if(counter != noOfLabels-1):
                text += 'and'
            counter += 1

        return text


    def get_detected_image(self,img):
        # Images
        imgs = [img]  # batched list of images

        # Inference
        results = self.model(imgs, size=416)  # includes NMS

        # Results
        results.print()  # print results to screen
        # results.show()  # display results
        # results.save()  # save as results1.jpg, results2.jpg... etc. in runs directory
        # print(results)  # models.common.Detections object, used for debugging

        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        n = len(labels)
        labelCnt = {}
        for i in range(n):
            classLabel = self.classes[int(labels[i])]
            row = cord[i]
            # row[4] is conf score
            print("{} is detected with {} probability.".format(classLabel, row[4]))
            if classLabel in labelCnt:
                labelCnt[classLabel] += 1
            else:
                labelCnt[classLabel] = 1

        text = self.get_text(labelCnt)
        print("{} This is from yolo_detection.py".format(text))
        # call gTTS (Google Text To Speech)
        

        # Data
        print('\n', results.xyxy[0])  # print img1 predictions
        #          x1 (pixels)  y1 (pixels)  x2 (pixels)  y2 (pixels)   confidence        class
        # tensor([[7.47613e+02, 4.01168e+01, 1.14978e+03, 7.12016e+02, 8.71210e-01, 0.00000e+00],
        #         [1.17464e+02, 1.96875e+02, 1.00145e+03, 7.11802e+02, 8.08795e-01, 0.00000e+00],
        #         [4.23969e+02, 4.30401e+02, 5.16833e+02, 7.20000e+02, 7.77376e-01, 2.70000e+01],
        #         [9.81310e+02, 3.10712e+02, 1.03111e+03, 4.19273e+02, 2.86850e-01, 2.70000e+01]])

        # Transform images with predictions from numpy arrays to base64 encoded images
        # array of original images (as np array) passed to model for inference
        results.imgs
        results.render()  # updates results.imgs with boxes and labels, returns nothing

        #for testing, display results using opencv
        """
        for img in results.imgs:
            cv2.imshow("YoloV5 Detection", cv2.resize(img, (416, 416))[:, :, ::-1])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        """
        
        return results.imgs[0],text





def run_model(img):
    '''
    obj = CurrencyNotesDetection(
        model_name='/home/gowtham/MajorProject/CurrencyNotesDetectionUsingYOLOv5/yolov5/runs/train/exp/weights/best.pt'
    )
    '''
    obj = CurrencyNotesDetection(
        model_name='./yolov5/runs/train/exp/weights/best.pt'
    )
    detected_labels_text = ""
    detected_img,detected_labels_text = obj.get_detected_image(img)
    return detected_img, detected_labels_text


