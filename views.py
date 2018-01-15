import datetime
import json

from django.contrib.auth import login
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView

from main_app.database_utils import get_tickets_sold, get_user_tickets
from main_app.excel_utils import generate_excel_tickets_sold, generate_excel_users
from main_app.forms import InsertFilmFromURLForm
from main_app.models import Film, FormularContact, Interval, Rezervare, Locuri
from main_app.utils import query_tmdb, get_current_week, get_date_interval, get_selectead_seats
from .forms import SignUpForm
from .models import Utilizator
from .utils import query_Youtube

()

base_img_url = 'https://image.tmdb.org/t/p/'
width = 'w185/'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def InsertFilmFromURL(request):
    if request.method == 'POST':
        form = InsertFilmFromURLForm(request.POST)
        if form.is_valid():
            result = query_tmdb(form.cleaned_data['url_IMDB'])
            dict = result['movie_results'][0]
            image_path = '%s%s' % (base_img_url, width)
            for key, value in dict.items():
                print(key, ' : ', value)
            film = Film(titlu=dict['title'],
                        descriere=dict['overview'],
                        data_lansare=dict['release_date'],
                        rating=dict['vote_average'],
                        link_IMDB=form.cleaned_data['url_IMDB'],
                        link_Youtube=form.cleaned_data['url_IMDB'],
                        imagine='%s%s' % (image_path, dict['poster_path']))
            film.save()
            return redirect('home')
    else:
        form = InsertFilmFromURLForm()
    return render(request, 'adauga.html', {'form': form})


def home(request):
    nr_saptamana, an, luni_date, duminica_date = get_current_week()
    azi = datetime.datetime.today()
    interval = Interval.objects.filter(nr_saptamana=nr_saptamana)
    interval_data = get_date_interval(azi, duminica_date)
    lista_filme_pk = [int(film.id_film.id) for film in interval]
    filme = Film.objects.filter(pk__in=lista_filme_pk)
    current_film = Film.objects.get(pk=3)
    generate_excel_tickets_sold()
    generate_excel_users()
    return render(request, 'index.htm',
                  {'filme': filme, 'current_film': current_film, 'interval_data': interval_data, 'luni': luni_date,
                   'duminica': duminica_date})


def my_account(request):
    return render(request, 'my_account.html')


def locuri_libere(request):
    locuri = request.GET.get('loc_selectat')
    lista_locuri_selectate = get_selectead_seats(locuri)
    utilizator = request.GET.get('utilizator')
    film_pk = request.GET.get("film_pk")
    data = request.GET.get("data")
    rezervare = Rezervare(persoana=utilizator,
                          data=data,
                          film=Film.objects.get(pk=int(film_pk)),
                          locuri_rezervate=' '.join(lista_locuri_selectate)
                          )
    rezervare.save()
    for loc in lista_locuri_selectate:
        ocupat = Locuri(film=Film.objects.get(pk=int(film_pk)),
                        data=data,
                        loc_ocupat=loc)
        ocupat.save()

    data = {
        'succes': lista_locuri_selectate
    }
    return JsonResponse(data)


def process_film(request, pk):
    nr_saptamana, an, luni_date, duminica_date = get_current_week()
    azi = datetime.datetime.today()
    interval_data = get_date_interval(azi, duminica_date)
    interval = Interval.objects.filter(nr_saptamana=nr_saptamana)
    lista_filme_pk = [int(film.id_film.id) for film in interval]
    filme = Film.objects.filter(pk__in=lista_filme_pk)
    film = Film.objects.get(pk=pk)
    return render(request, 'index.htm',
                  {'filme': filme, 'current_film': film, 'interval_data': interval_data, 'luni': luni_date,
                   'duminica': duminica_date})


class AccountUpdate(UpdateView):
    model = Utilizator
    fields = ('first_name', 'last_name', 'data_nasterii', 'gender',)
    context_object_name = 'accountUpdate'
    template_name = 'update_account.html'

    def form_valid(self, form):
        user = form.save()
        user.save()
        return redirect('myAccount')


def contact(request):
    if request.method == 'GET':
        nume = request.GET['nume_complet']
        email = request.GET['email']
        mesaj = request.GET['message']
        contact = FormularContact(nume=nume, email=email, mesaj=mesaj)
        contact.save()
    return redirect('home')


def afiseaza_film(request):
    film = request.GET.get('film_pk')
    data = request.GET.get('data')
    locuri_ocupate = []
    found = Locuri.objects.filter(film=Film.objects.get(pk=int(film)),
                                  data=data)
    for loc in found:
        locuri_ocupate.append(loc.loc_ocupat)
    locuri = {
        'locuri_ocupate': locuri_ocupate
    }
    return JsonResponse(locuri)


def redirecteaza(request):
    titlu = request.GET.get('titlu')
    film = Film.objects.get(titlu=titlu)
    film_pk = film.pk
    data = {
        'gasit': film_pk
    }
    return JsonResponse(data)


def afiseaza_rezervari(request, pk):
    azi = datetime.datetime.today()
    nume_utilizator = Utilizator.objects.get(pk=int(pk))
    rezervari = Rezervare.objects.filter(persoana=nume_utilizator.username)
    return render(request, 'rezervari.html',
                  {'rezervari': rezervari,
                   'azi': azi})


def sterge_rezervare(request):
    id_rezervare = request.GET.get('id_rezervare')
    rezervare = Rezervare.objects.get(pk=int(id_rezervare))
    locuri_ocupate = rezervare.locuri_rezervate.split(' ')
    loc_de_sters = Locuri.objects.filter(loc_ocupat__in=locuri_ocupate)
    loc_de_sters.delete()
    rezervare.delete()
    data = {
        'found': rezervare.locuri_rezervate
    }
    return JsonResponse(data)
