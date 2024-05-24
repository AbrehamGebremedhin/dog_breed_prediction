from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from model import Predict
from pathlib import Path
from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv('breed_prediction\config.env')

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
                file_path)

            return render({"breed": breed['predicted_breed'],
                           "percentage": breed['percentage'],
                           'path': f"static\images\{image_file.name}"})

    return render(request, 'home/home.html')


# Create your views here.
def apiResponse(request):
    if request.method == 'POST':
        client = MongoClient(os.getenv('link'))
        db = client["dog_breed_identification"]
        document = db["dog_breed_information"]

        image_file = request.FILES.get('image')
        if image_file:
            # Save the image locally
            default_storage.save(
                f'{image_file.name}', ContentFile(image_file.read()))

            file_path = f"D:\Projects\dog_breed_prediction\static\images\{image_file.name}"

            breed = predict.predict_image(
                file_path)

            information = document.find_one(
                {"breed": breed['predicted_breed']})

            return JsonResponse({"breed": breed['predicted_breed'],
                                 "percentage": breed['percentage'],
                                 "info": information['information'],
                                 "size": information['size'],
                                 "temperament": information['temperament'],
                                 "exercise_needs": information['exercise_needs'],
                                 "suitability": information['suitability'],
                                 "shedding": information[' shedding_tendencies'],
                                 "trainability": information['trainability'],
                                 "lifespan": information['lifespan']})
        else:
            # No image file provided in the request
            return JsonResponse({"error": "No image file provided"})
    else:
        # Request method is not POST
        return JsonResponse({"error": "Only POST requests are allowed"})
