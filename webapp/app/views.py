from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import cv2
from django.conf import settings
from .face_detection_dnn import image_converter

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
        output_path = settings.BASE_DIR + obj.output.url
        a = image_converter(input_path, output_path, threshold=int(1), convert_mode=int(1))
        print(a)

    return render(request, 'app/index.html', {
        'form': form,
        'obj':obj,
    })
