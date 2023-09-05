from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .lib import apk_analysis

# Create your views here.

def index(request):
    return render(request, 'index.html', {'title':'Anasayfa'})

def upload_file(request):
    if (request.method == 'POST'):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_info = request.FILES['app_file']
            fs = FileSystemStorage()
            filename = fs.save(file_info.name, file_info)
            uploaded_file_url = fs.url(filename)
            result = apk_analysis.apk_anaysis(f"{settings.BASE_DIR}{uploaded_file_url}")

            return render(request, 'result.html', {'result':result})
        else:
            form = UploadFileForm()
        return HttpResponse('Dosya yüklendi')