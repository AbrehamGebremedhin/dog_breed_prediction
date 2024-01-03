from django.shortcuts import render
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from model import Predict
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

predict = Predict()


# Create your views here.
def home(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if image_file:
            # Save the image locally
            default_storage.save(
                f'{image_file.name}', ContentFile(image_file.read()))

            file_path = f"D:\Projects\dog_breed_prediction\static\images\{image_file.name}"

            breed = predict.predict_image(
                [file_path])

            return render(request, 'home/result.html', {"breed": breed['predicted_breed'],
                                                        "percentage": breed['percentage'],
                                                        'path': f"static\images\{image_file.name}"})

    return render(request, 'home/home.html')
