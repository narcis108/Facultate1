from django.db.models.aggregates import Sum, Count

from main_app.models import Locuri, Film, Rezervare


def get_tickets_sold():
    locuri_vandute = Locuri.objects.values('film').annotate(Count('loc_ocupat'))
    return locuri_vandute


def get_user_tickets():
    bilete_cumparate = Rezervare.objects.values('persoana').annotate(Count('locuri_rezervate'))
    return bilete_cumparate