# Ajouté pour l'app Django debug toolbar
from django.conf import settings
from django.conf.urls import include, url

# Initialement
from django.contrib import admin
#from django.conf.urls import url

from store import views

urlpatterns = [
    url(r'^$', views.index, name="index"),          # name="index" : j'ai nommé la vue pour effectuer des tests en l'appelant par son nom
    url(r'^securite-admin/', admin.site.urls),
    # La methode url associe un shema de route à un ensemble de vue.
    # elle prend en premier parametre une expression reguliere representant un shema
    #            et en second parametre la vue à associer
    # ici la methode url va ajouter toutes les urls contenu dans urls.py de store en les prefixant par store/
    url(r'^store/', include('store.urls', namespace='store')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns