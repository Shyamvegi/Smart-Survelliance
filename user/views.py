from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages

######Detection Modules ########################

import torch
import cv2
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core.mail import EmailMessage,send_mail
from django.template.loader import render_to_string
from GunDetection import settings
#################################################


def index(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['uname'] if 'uname' in request.POST else None
        password = request.POST['psd']
        print(username,password)
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/home')
        else:
            print("Invalid User")
            messages.info(request,'Invalid username or passsword')
    return render(request,'user/index.html')
def register(request):
    if request.method == 'POST':

        email = request.POST['mail']
        username = request.POST['uname']
        password= request.POST['psd']
        user = User.objects.create_user(username = username , password = password , email = email)
        user.save()

        print('user created')
        return redirect('/home')
    return render(request,'user/register.html')
def logoutUser(request):
    auth.logout(request)
    return render(request,'user/index.html')
def home(request):
    return render(request,'user/home.html')




############################# Detection Code ###########################################################################
dest = False
now = None
target = None
class GunDetection:
    def __del__(self):
        self.cap.release()
    def __init__(self, capture_index, model_name):
        self.capture_index = capture_index
        self.model = self.load_model(model_name)
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.cap = cv2.VideoCapture(self.capture_index)
    def load_model(self, model_name):
        if model_name:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_name, force_reload=True)
        else:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        return model

    def score_frame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord

    def class_to_label(self, x):
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        global now
        global target
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.45:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
                if now is None or datetime.now()>target:
                    now = datetime.now()
                    print(now)
                    target = now + timedelta(minutes=1)
                    cv2.imwrite("detected-frame.jpg",frame)
                    toEmail1 = "shyamvegi16@gmail.com"
                    sub = "Alert Weapon Detected"
                    msg = render_to_string('user/mail_template.html',{
                    
                    })
                    email = EmailMessage(sub,msg,settings.EMAIL_HOST_USER,[toEmail1])
                    email.fail_silently = True
                    email.attach_file(str(settings.BASE_DIR)+"\\detected-frame.jpg")
                    email.content_subtype = "html"
                    email.send()
                    print("Email Sent <3 ")
        return frame

    def __call__(self):
        global now
        global target
        assert self.cap.isOpened()      
        while True:          
            ret, frame = self.cap.read()
            assert ret
            tFrame = frame
            frame = cv2.resize(frame, (416,416))
            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)
            cv2.imshow('YOLOv5 Detection', frame)
            
            if cv2.waitKey(1) & 0xFF == 27:
                break
            
def performAction(request):
    actn = request.GET.get("action")
    response = {
        'actn': actn
         }
    detector = GunDetection(capture_index=0, model_name='C:\\Users\\vicky\\Desktop\\GunDetection\\GunDetection\\static\\best.pt')
    if actn=="init":
        detector()
        response['actn'] = "Monitoring Started"
    else:
        del detector
        response['actn'] = "Monitoring Stopped"
        print("Destroyed...")
    return JsonResponse(response)
    
###################################################################################################################