from functools import reduce
import os
import uuid
from collections import OrderedDict
import firebase_admin
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from firebase_admin import auth, firestore, db, credentials
from werkzeug.security import check_password_hash
from firebase_admin import initialize_app

cred = credentials.Certificate('irrigation//firebase.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://irrigatic-177d1-default-rtdb.firebaseio.com'
})


ref = db.reference('/')



def HomePage(request):
    return render (request,'home.html')


def SignIn(request: HttpRequest):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('mdp')
        # try:
        user = auth.get_user_by_email(email)
        print(user.uid)
        request.session.setdefault('user_uid', user.uid)
        if email == 'admin@caustaza.com' and password == '123456':
            return redirect('admin_home')
        return redirect('home')
    

        # except auth as e:
        #     error_message = "Invalid email or password."
        #     messages.error(request, error_message)
        # except Exception as __e:
        #     ...

    return render(request, 'signIn.html')






def admin_home(request):
    return render(request, 'admin_home.html')







def Logout(request):
    logout(request)
    return redirect('signin')




from django.shortcuts import redirect, render
from firebase_admin import auth, db


def SignUp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('mdp')
        confirmMdp = request.POST.get('confirmMdp')
        date = request.POST.get('date')
        genre = request.POST.get('genre')
        tel = request.POST.get('tel')
        

        try:
            user = auth.create_user(
                email=email,
                password=password,
            )
            
            user_data_ref = db.reference('users/' + user.uid)
            user_data_ref.set({
                'email': email,
                'date': date,
                'genre': genre,
                'tel': tel,
            })

            messages.success(request, "User created successfully.")
            return redirect('signin')

        except auth.AuthError as e:
            error_message = "Failed to create user: " + str(e)
            messages.error(request, error_message)

    return render(request, 'signUp.html')




User = get_user_model()

def ForgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email') 

        try:
            user = auth.get_user_by_email(email)
        except auth.AuthError as e:
            messages.error(request, 'Aucun utilisateur avec cet email n\'existe.')
            return render(request, 'forget_password.html')

        auth.generate_password_reset_link(email)

        messages.success(request, 'Un email de réinitialisation du mot de passe a été envoyé.')
        return render(request, 'forget_password.html')

    return render(request, 'forget_password.html')


def ChangePassword(request, token):
    if request.method == 'POST':
        password = request.POST['password']
        
        try:
            user_id = auth.verify_password_reset_link(token, request.get_full_path())
            auth.update_user(user_id, password=password)
            messages.success(request, 'Votre mot de passe a été réinitialisé avec succès.')
            return redirect('password_changed')
        except auth.AuthError as e:
            messages.error(request, 'Une erreur s\'est produite. Veuillez réessayer plus tard.')

    return render(request, 'change_password.html', {'token': token})

import json

from django.shortcuts import render
from firebase_admin import db


def guide(request):
    plants = db.reference('plants').get().values()

    context = {
        'plants': plants
    }
    return render(request, 'guide.html', context)


import json

from .models import PlantForm


def ajouter_plante(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.image = request.FILES.get('image')
            plant_data = {
                'ideal_humidity': plant.ideal_humidity,
                'ideal_temperature': plant.ideal_temperature,
                'irrigation_frequency': plant.irrigation_frequency,
                'name': plant.name,
                'ph_level': plant.ph_level,
                'plant_type': plant.plant_type,
                'planting_date': plant.planting_date.isoformat(),
                'tree_spacing': plant.tree_spacing,
                'trees_per_hectare': plant.trees_per_hectare,
                'nbre_des_valves':plant.nbre_valve,
            }
            
            serialized_plant_data = json.dumps(plant_data)
            db.reference("plants").push(serialized_plant_data)
            return redirect('admin_home')
    else:
        form = PlantForm()
    
    return render(request, 'ajouter_plante.html', {'form': form})


import json

from .models import Farm, FarmForm


def mesespaces(request: HttpRequest):
    farms = db.reference('/farms').get()
    
    return render(request, 'mesespaces.html', {'farms': farms})



from django.shortcuts import redirect, render
from firebase_admin import db


def ajouter_ferme(request):
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            uid = request.session.get('user_uid')
            farm.user = uid
            farm.surface = float(farm.surface)
            
            farm_data = {
                "farm_name": farm.farm_name,
                "location": farm.location,
                "surface": farm.surface,
                "user": str(farm.user)
            }
            
            db.reference("farms").push(farm_data)
            
            return redirect('mesespaces')
    else:
        form = FarmForm()
    
    return render(request, 'ajouter_ferme.html', {'form': form})
    







def supprimer_ferme(request, farm_id):
    farm_ref = db.reference('farms')
    
    if request.method == 'POST':
        farm_ref.child(farm_id).delete()
        return redirect('home')
    
    farm_data = farm_ref.child(farm_id).get()
    
    if farm_data is None:
        return redirect('home')
    
    farm = {
        'id': farm_id,
        'farm_name': farm_data.get('farm_name'),
        'location': farm_data.get('location'),
        'surface': farm_data.get('surface'),
        'user': farm_data.get('user')
    }
    
    return render(request, 'supprimer_ferme.html', {'farm': farm})




import firebase_admin
from firebase_admin import db

from .models import Zone, ZoneForm


def zones_view(request: HttpRequest, farm_id):
    zones=db.reference('/zones').order_by_child('farm_id').equal_to(farm_id).get()
    context = {
        'zones': zones,
        'farm_id': farm_id
    }

    return render(request, 'zones.html', context)



def create_sensors(zone_id):
   
    ref = db.reference('/')

    
    capteur_temperature = {
        'zone_id': zone_id,
        'valeur': 0.0  
    }
    ref.child('capteur_temperature').push(capteur_temperature)

    capteur_humidite = {
        'zone_id': zone_id,
        'valeur': 0.0  
    }
    ref.child('capteur_humidite').push(capteur_humidite)


def dash(request: HttpRequest, farm_id, zone_id):
    ref = db.reference('/')
    capteur_humidite_ref = ref('/capteur_humidite')
    capteur_temperature_ref = ref('/capteur_temperature')

    capteur_humidite_values = capteur_humidite_ref.child(farm_id).child(zone_id).get()
    capteur_temperature_values = capteur_temperature_ref.child(farm_id).child(zone_id).get()

    context = {
        'farm_id': farm_id,
        'zone_id': zone_id,
        'capteur_humidite_values': capteur_humidite_values,
        'capteur_temperature_values': capteur_temperature_values,
    }

    return render(request, 'dash.html', context)



import json

from django.contrib import messages

from .models import ZoneForm


def ajouter_zone(request: HttpRequest, farm_id):
    related_farm = db.reference('/farms').order_by_key().equal_to(farm_id).get().get(farm_id)
    related_farm_zones = db.reference('/zones').order_by_child('farm_id').equal_to(farm_id).get()
    zones_data = [x for x in related_farm_zones.values()]
    existant_surfaces_sum = sum([x.get('surface', 0) for x in zones_data])
    # surfaces_existantes = sum(list(map(lambda zone: zone.get('surface', 0), zones_existantes)))
    # farm_surface = 
    form = ZoneForm()
    surface_farm = related_farm['surface']
    if request.method == 'POST':
        form = ZoneForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Le formulaire n'est pas valide.")
            form = ZoneForm()
            return redirect('ajouter_zone', farm_id)
        zone = form.save(commit=False)
        # to add a zone, the surface of the new zone, aggregated with existed zones must not exceed the farm surface
        if float(zone.surface) + existant_surfaces_sum > surface_farm:
            messages.error(request, f"La surface totale des zones dépasse la surface de la ferme.({surface_farm} Ha)")
            return redirect('ajouter_zone', farm_id)
        zone_data = {
            "farm_id": farm_id,
            "name": zone.name,
            "surface": float(zone.surface),
            "nom_plante": zone.nom_plante,
            "type_plante": zone.type_plante,
            "type_plantation": zone.type_plantation,
            "nombre_portes": zone.nombre_portes,
        }
        zone_ref=db.reference('/zones').push(zone_data)
        create_sensors(zone_ref.key)


        return redirect('zones', farm_id)

    context = {
        'form': form
    }
    return render(request, 'ajouter_zone.html', context)




from django.shortcuts import render, get_object_or_404
from .models import Zone, CapteurTemperature, Plant
def afficher_temperature_humidite(request, zone_id):
    zone = get_object_or_404(Zone, pk=zone_id)
    capteurs_temperature = CapteurTemperature.objects.filter(zone=zone)
    plant = Plant.objects.get(name=zone.nom_plante)

    temperature_ideale_plante = plant.ideal_temperature
    humidite_ideale_plante = plant.ideal_humidity

    # Récupérer les données de température depuis Firebase Realtime Database
    temperature_ref = db.reference('zones/{}/capteur_temperature'.format(zone_id))
    temperature_snap = temperature_ref.get()
    if temperature_snap:
        temperatures = temperature_snap.values()
    else:
        temperatures = []

    # Récupérer les données d'humidité depuis Firebase Realtime Database
    humidite_ref = db.reference('zones/{}/capteur_humidite'.format(zone_id))
    humidite_snap = humidite_ref.get()
    if humidite_snap:
        humidites = humidite_snap.values()
    else:
        humidites = []

    # Vérifier les conditions pour activer les boutons de valves
    is_temperature_above_ideale = any(temp > temperature_ideale_plante for temp in temperatures)
    is_humidite_below_ideale = any(humid < humidite_ideale_plante for humid in humidites)

    context = {
        'zone': zone,
        'capteurs_temperature': capteurs_temperature,
        'temperature_ideale_plante': temperature_ideale_plante,
        'humidite_ideale_plante': humidite_ideale_plante,
        'temperatures': temperatures,
        'humidites': humidites,
        'is_temperature_above_ideale': is_temperature_above_ideale,
        'is_humidite_below_ideale': is_humidite_below_ideale
    }

    return render(request, 'dash.html', context)


