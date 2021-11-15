# Import de toutes les urls qui font partie du projet
from django.conf.urls import url

# Import de toutes les vues de l'application
from . import views

# Déclaration
app_name='store'
urlpatterns = [
# Ici, si une url commence ou finit par une chaine vide, elle est reliée à la vue listing
    url(r'^$', views.listing, name="listing"),
# Ensuite, si l'url comprend une suite de chiffre, elle affichera la vue donnée par la fonction detail
    # la fonction "detail"prendra comme argument "album_id" en plus de la requete
    # Le fait d'ecrire en toute lettre ce qui se trouve entre les symboles ?P< > permet de passer les parametres à la vue
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'^search/$', views.search, name="search"),
]
# Le fait d'attribuer un parametre name dans la méthode name nous permettra de :
#           -faire explicitement référence à la vue associée avec "name" plutôt qu'en renseignant l'adresse url
#            (/store/2 )quand on voudra insérer un lien dans une page html
#               --> permet d'éviter d'être dependant de son shéma d'url en cas de modif par exemple