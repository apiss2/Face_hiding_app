from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import cv2
from django.conf import settings

def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DocumentForm()
        max_id = Document.objects.latest('id').id
        obj = Document.objects.get(id = max_id)
        input_path = settings.BASE_DIR + obj.photo.url
        output_path = settings.BASE_DIR + "/media/output/output.jpg"
        gray(input_path,output_path)

    return render(request, 'app/index.html', {
        'form': form,
        'obj':obj,
    })


###########ここをカスタマイズ############

def gray(input_path,output_path):
    img = cv2.imread(input_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(output_path, img_gray)

######################################