from django.shortcuts import render,redirect

# Create your views here.
from .form import FileUploadForm
from .ocr import extract_data
import csv 

def index(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            file_name = uploaded_file.name
            print("File Name",file_name)
            form.save()
            extract_data(file_name)
            with open(f'csv_files/{file_name[:-4]}.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                data.pop(0)
                data.pop(1)
            
            

            return render(request,'index.html',{'csv':data})
    else:
        form = FileUploadForm()
    return render(request, 'index.html', {'form': form})


    



def pdf_extraction():
    pass 