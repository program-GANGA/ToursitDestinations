from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import generics
from .serializers import *
from rest_framework.permissions import AllowAny
from .models import *
import requests
from django.contrib import messages
from requests.exceptions import RequestException
from django.core.paginator import Paginator
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import TouristDes
from .serializers import TouristDesSerializer

class TouristCreateView(generics.ListCreateAPIView):
    queryset = TouristDes.objects.all()
    serializer_class=TouristDesSerializer
    permission_classes=[AllowAny]

class TouristDetailsView(generics.RetrieveAPIView):
    queryset = TouristDes.objects.all()
    serializer_class = TouristDesSerializer

class TouristUpdateView(generics.RetrieveUpdateAPIView):
    queryset = TouristDes.objects.all()
    serializer_class = TouristDesSerializer

class TouristDeleteView(generics.RetrieveDestroyAPIView):
    queryset = TouristDes.objects.all()
    serializer_class = TouristDesSerializer

class TouristSearch(generics.ListAPIView):
    queryset=TouristDes.objects.all()
    serializer_class=TouristDesSerializer
    def get_queryset(self):
       placename=self.kwargs.get('placename')
       return TouristDes.objects.filter(placename__icontains=placename)
 

def create_tour(request):
    if request.method == 'POST':
        data = {
            'placename': request.POST.get('placename'),
            'weather': request.POST.get('weather'),
            'state': request.POST.get('state'),
            'district': request.POST.get('district'),
            'maplink': request.POST.get('maplink'),
            'description': request.POST.get('description')
        }
        images = request.FILES.getlist('img')
        files = [('img', img) for img in images]
        try:
            api_url = 'http://127.0.0.1:8000/create/' 
            response = requests.post(api_url, data=data, files=files)
            print("API Response Status Code:", response.status_code)
            print("API Response Content:", response.content)
            if response.status_code == 201:
                messages.success(request, 'Tourist destination created successfully!')
                return redirect('/') 
            else:
                messages.error(request, f'Error in adding the place: {response.content.decode()}')
        except RequestException as e:
            messages.error(request, f'Error during API request: {str(e)}')
    return render(request, 'create.html')



def index(request):
    data = []
    page_obj = None
    api_url = 'http://127.0.0.1:8000/create/'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            org_data=data
            if not data:
                messages.warning(request, 'No data available.')
            else:
                paginator = Paginator(org_data, 4)
                page_number = request.GET.get('page', 1)
                page_obj = paginator.get_page(page_number)
        else:
            messages.error(request, 'Error retrieving tourist destinations.')
    except RequestException:
        messages.error(request, 'Network error while fetching data.')

    return render(request, 'index.html', {'page_obj': page_obj, 'data': data})



def tourist_detail(request, id):
    api_url = f'http://127.0.0.1:8000/detail/{id}/' 
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            tourist_instance = get_object_or_404(TouristDes, id=id)
            all_images = tourist_instance.additional_images.all()
            
            if request.method == 'POST' and 'additional_images' in request.FILES:
                for image in request.FILES.getlist('additional_images'):
                    TouristImage.objects.create(tourist_des=tourist_instance, image=image)
                messages.success(request, 'Images uploaded successfully.')
                return redirect('detail', id=id)
            
            return render(request, 'detail.html', {'data': data, 'all_images': all_images})
        else:
            messages.error(request, 'Error retrieving tourist details.')
    except RequestException:
        messages.error(request, 'Network error while fetching details.')

    return render(request, 'detail.html', {'data': None, 'all_images': []})


 
def tourist_update(request, id):
    api_url = f'http://127.0.0.1:8000/update/{id}/'
    tourist = get_object_or_404(TouristDes, id=id)  
    if request.method == 'POST':
        data = {
            'placename': request.POST.get('placename'),
            'weather': request.POST.get('weather'),
            'state': request.POST.get('state'),
            'district': request.POST.get('district'),
            'maplink': request.POST.get('maplink'),
            'description': request.POST.get('description'),
        }
        files = {'img': request.FILES['img']} if 'img' in request.FILES else None
        response = requests.patch(api_url, data=data, files=files)
        if response.status_code == 200:
            messages.success(request, 'Tourist destination updated successfully!')
            return redirect('base')  
        else:
            messages.error(request, 'Failed to update the tourist destination.')
    return render(request, 'update.html', {'tourist': tourist})




        

def tourist_delete(request, id):
    api_url = f'http://127.0.0.1:8000/delete/{id}/' 
    try:
        response = requests.delete(api_url)
        if response.status_code == 200:
            messages.success(request, 'Tourist destination deleted successfully.')
        else:
            messages.error(request, 'Failed to delete the tourist destination. Please try again.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('base')
    


                

        








    


    

