from .models import classify
from pathlib import Path
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from os import path
from django.shortcuts import render
import sys
from .fetch import get_data
from .util import classify_image
sys.path.append(path.join(path.dirname(__file__), '..'))
BASE_DIR = Path(__file__).resolve().parent.parent


@login_required
def dashboard(request):
    usr = request.user
    data = classify.objects.filter(user=usr).order_by('-id')
    context = {
        'data': data
    }
    return render(request, 'dashboard.html', context=context)


@login_required
def weather(request):
    return render(request, 'virtual-reality.html')


treatment = {
    "Corn": {
        "Blight": "Treating Corn leaf blight involves using fungicides. The infection usually begins around the time of silking, and this is when the fungicide should be applied.",
        "Common_Rust": "Treating Common Rust involves using fungicides. Some organic fungicides may also work.",
        "Gray_Leaf_Spot": "Gray leaf spot lesions on corn leaves hinder photosynthetic activity, reducing carbohydrates allocated towards grain fill. Planting hybrids with a high level of genetic resistance can help reduce the risk of yield loss due to gray leaf spot infection.",
        "Healthy": "Your Corn Plant is Healthy. Just make sure to water your plant daily and it should remain healthy."
    },
    "Pepper_Bell": {
        "Bacterial_Spot": "You should uproot the plant as soon as possible. Leaving it on the surface will make other plants susceptible to infection. Deal with the root cause of the problem before it spreads.",
        "Healthy": "Your Pepper Bell plant is Healthy. Just make sure to water your plant daily and it should remain healthy."
    },
    "Potato": {
        "Early_Blight": "If only a few leaves are infected, you can remove them and dispose of them under the soil otherwise use Fungicides.",
        "Healthy": "Your Potato Plant is Healthy. Just make sure to water your plant daily and it should remain healthy.",
        "Late_Blight": "The treatment of late blight in potatoes involves spraying the crop with foliar fungicides. Apply scheduled sprays, in order to avoid the disease from developing."
    },
    "Tomato": {
        "Late_Blight": "If only a few leaves are infected, you can remove them and dispose of them under the soil otherwise try copper spray",
        "Healthy": "Your Tomato Plant is Healthy. Just make sure to water your plant daily and it should remain healthy.",
        "Bacterial_Spot": "A plant with bacterial spot cannot be cured. Remove symptomatic plants from the field or greenhouse to prevent the spread of bacteria to healthy plants.",
        "Early_Blight": "Use pathogen-free seed, or collect seed only from disease-free plants. Rotate out of tomatoes and related crops for at least two years. ",
        "Leaf_Mold": "Applying fungicides when symptoms first appear can reduce the spread of the leaf mold fungus significantly. Several fungicides are labeled for leaf mold control on tomatoes and can provide good disease control if applied to all the foliage of the plant, especially the lower surfaces of the leaves.",
        "Mosaic_Virus": "Fungicides will NOT treat this viral disease. Plant resistant varieties when available or purchase transplants from a reputable source.",
        "Septoria_Leaf_Spot": "Remove diseased leaves. Improve air circulation around the plants.",
        "Spider_Mites": "Extension horticulturists currently recommend aiming a hard stream of water at infested plants to knock spider mites off the plants.",
        "Target_Spot": "Remove old plant debris at the end of the growing season; otherwise, the spores will travel from debris to newly planted tomatoes in the following growing season, thus beginning the disease anew.",
        "YellowLeaf__Curl_Virus": "Other methods to control the spread of TYLCV include planting resistant/tolerant lines, crop rotation, and breeding for resistance of TYLCV."
    }
}


@login_required
def test(request):
    if request.method == 'POST':
        if request.FILES['myfile']:
            usr = request.user
            temp = classify()
            temp.user = usr
            myfile = request.FILES['myfile']
            fs = FileSystemStorage(location='media/model')
            filename = fs.save(myfile.name, myfile)
            print(str(BASE_DIR)+'/media/model/'+filename)
            data = classify_image(str(BASE_DIR)+'/media/model/'+filename)
            typ = data['plant']
            acc = data['probablity']
            dis = data['status']
            temp.disease = dis
            temp.accuracy = acc
            temp.img = filename
            temp.plant_name = typ
            temp.treatment = treatment[data['plant']][data['status']]
            temp.save()
            return redirect(dashboard)
    return render(request, 'billing.html')


@login_required
def plants(request):
    context = {
        'data': get_data()
    }
    return render(request, 'tables.html', context=context)
