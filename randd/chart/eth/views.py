import pandas as pd
import matplotlib.pyplot as plt
import io
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import UploadedFile

def handle_uploaded_file(f):
    try:
        file_content = f.read().decode('utf-8')
        print("File content:", file_content)  
        f.seek(0)  
        df = pd.read_csv(f)
        if df.empty:
            raise ValueError("The file is empty or does not contain valid data.")
        fig, ax = plt.subplots()
        # ax = plt.axes(projection="3d")
        df.plot(ax=ax)
        buf = io.BytesIO()
        # plt.grid(True)
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf
    except pd.errors.EmptyDataError:
        raise ValueError("No columns to parse from file")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            try:
                buf = handle_uploaded_file(request.FILES['file'])
                return HttpResponse(buf, content_type='image/png')
            except ValueError as e:
                return HttpResponse(f"Error: {e}", status=400)
        else:
            return HttpResponse(f"Form is invalid: {form.errors}", status=400)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
