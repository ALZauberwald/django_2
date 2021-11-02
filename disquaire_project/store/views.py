from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Album, Artist, Contact, Booking
from .forms import ContactForm, ParagraphErrorList
from django.db import transaction, IntegrityError

# On importe le module loader qui sera utile pour charger le gabarit souhaité pour afficher une vue
from django.template import loader

def index(request):
    # Dans l'index le but est d'afficher la liste des 5 derniers ajouts d'album

    # Je cré une variable albums qui recupere gràce à objects.filter tous les albums (où available est True)
    #                                   .order_by() me permet de trier leur ordre d'affichage
    #                                    [:5] indique le nombre d'élément à afficher
    albums= Album.objects.filter(available=True).order_by('-created_at')[:5]
    # Je m'occupe maintenant du formatage de l'affichage de ma requète
    # 1/2. Je cré une liste pour y stocker les balises html et le contenu de ce que je souhaite voir s'afficher "formatted_albums"
    #       Pour chaque album que j'ai stocké dans albums, j'insère donc les balises html <li>
    #               dans lesquelles j'insère également le nom de l'album
    formatted_albums= ["<li>{}</li>".format(album.title) for album in albums]
    # 2/2 Je déclare les balises html de liste dans "message" et j'y intègre dedans les lignes de la liste  formatted_albums
    message ="""<ul>{}</ul>""".format("\n".join(formatted_albums))

    # Pour charger le gabarit du theme
    template = loader.get_template('store/index.html')

    # par convention on nomme context les variables renseignées dans le dictionnaire de render
    context = {'albums': albums}
    return HttpResponse(template.render(context, request=request)) # render peut prendre en premier parametre un dictionnaire de variable qu'on lui associe


def listing(request):
    # Dans cette vue, tous les albums doivent s'afficher
    albums_list = Album.objects.filter(available=True)
    paginator= Paginator(albums_list, 6) # on déclare paginator comme une instance de Paginator
    # paginator cré automatiquement un nouveau dictionnaire dans l'url avec 'page' comme clez
    page= request.GET.get('page')    # paginator se situe en recuperant la valeur de page
    try:
        albums = paginator.page(page)   # paginator prend note des elements a afficher en fonction du numéro page
    except PageNotAnInteger :
        albums =paginator.page(1)    # premiere page renvoyée
    except EmptyPage:
        albums= Paginator.page(paginator.num_pages) # derniere page renvoyée
    #template = loader.get_template('store/index.html')
    context ={
        'albums':albums,
        'paginate':True   # cette variable sera utilisée dans les gabarits pour verifier qu'il faut utiliser paginator

    }
    #return HttpResponse(template.render(context, request=request))

    # render remplace template et HttpResponse en raccourcissant le code
    return render(request, 'store/listing.html', context)

@transaction.atomic
def detail(request, album_id):
    # L'objectif de cette vue c'est d'afficher l'album souhaitée et les artistes qui y sont associés
    # ainsi que le formulaire à compléter et ses variantes en fonction des entrées erronées de l'utilisateur

    # Quand detail est appelé, la barre d'url renseignée par l'utilisateur contient album_id
    #  l'url est en effet générée sous cette forme '^(?P<album_id>[0-9]+)/$
    # La fonction get() permet donc d'utiliser album_id, pour chercher dans la bdd l'information souhaitee
    # album = Album.objects.get(pk=album_id)
    # La fonction get_object_or_404 fait pareil mais va chercher la 404.html si l'element cherché n'est pas trouvé
    album = get_object_or_404(Album, pk=album_id)
    artists = [artist.name for artist in album.artists.all()]
    artists_name = " ".join(artists)
    # La méthode join() prend tous les éléments d'un itérable et les joint en une seule chaîne.
    # Une chaîne doit être spécifiée comme séparateur. (ici la chaine est " " espace)
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'album_picture': album.picture
    }
    if request.method == 'POST':
        # l'objectif : si la page détail s'affiche suite à la soumission d'un formulaire
        # enregistre les infs entrées par l'ut qui se trouvent dans les parametres de la requete
        # request.POST.get('inf')

        #On commence par effectuer une seconde vérification des informations entrées par l'utilisateur
        form = ContactForm(request.POST, error_class=ParagraphErrorList)# on precise error_class dans le but de customiser
                                                                        # l'affichage des erreurs (ParagraphErrorList est
                                                                        # une classe que nous avons créée dans .forms)
        if form.is_valid():
            try:
                email = request.POST.get('email')
                name = request.POST.get('name')
                # maintenant on va regarder si le contact existe, s'il n'existe pas on le créé
                contact = Contact.objects.filter(email=email)
                if not contact.exists():
                    contact = Contact.objects.create(
                        email=email,
                        name=name
                    )
                else :
                    # si le contact existe deja , on a besoin de contact sous forme d'objet contact et non queryset(liste)
                    contact = contact.first() # on recupere donc la premiere valeur de la queryset
                                                # (c'est filtré par mail donc la liste d'objet contact contenu dans la query set est certainement egal à un)


                # on va ensuite checker l'album.
                album = get_object_or_404(Album, id=album_id)
                #si tout va bien , alors on cré une réservation
                booking = Booking.objects.create(
                    contact=contact,
                    album=album
                )

                album.available = False #l'album n'est plus disponible
                album.save()
                context = {
                    'album_title': album.title
                }
                #on dirige pour finir l'utilisateur vers un template de remerciement
                return render(request, 'store/merci.html', context)
            except IntegrityError:
                form.errors['internal'] = "Une erreur interne est survenue, veuillez accepter nos excuses. Vous pouvez, si vous " \
                                  "le désirer effectuer une autre requète."
                context['errors'] = form.errors.items()
        else: # si le formulaire n'est pas valide, je transmet au contexte les erreurs pour qu'il puisse les afficher
            context['errors'] = form.errors.items()
    else: # on genere une instance de formulaire si aucun formulaire n'a encore été soumis (type get)
        form = ContactForm()

    context['form'] = form # on ajoute dans le contexte le formulaire
    #le programme n'arrivera à ces lignes que si la requete est de type get ou si le formulaire n'est pas valide
    # On pourrait synthétiser les erreurs et declarer ici : context['errors'] = form.errors.items()
    return render(request, 'store/detail.html', context)


def search(request):
    # L'objet Request est une instance de la classe wsgirequest
    # Il a des proprietes interessantes, notamment GET
    # --> renvoi un dictionnaire contennant tous les parametres contenus dans l'url
    query = request.GET.get('query') #--> on demande à récupérer les valeurs en fonction de la clez 'query' ('query' correspond au name de l'input déclaré dans le formulaire html et transmis dans l'url)
    if not query:
        # Cela signifie :"Aucun artiste renseigné dans la requète"
        # A ce moment là, il semble interessant de renvoyer la liste de tous les albums
        albums = Album.objects.all()
    else :
        # L'utilisateur veut "query", donnons le lui
        albums = Album.objects.filter(title__icontains=query)
        #__contains permet de preciser qu'on veut recupere l'album si il contient simplement query
        #__icontains permet la meme chose mais en n'étant pas sensible à la casse

        # Par contre on est pas sur que "query" soit reellement un titre d'album,
        # Interessant d'approfondir si l'utilisateur a rentré un artiste
        if not albums.exists():
            # rappel : la variable artists est une relation manytomany déclarée --> contient donc le nom des artists associés
            albums = Album.objects.filter(artists__name__icontains=query)


    context = {
        'query': query,
        'albums': albums
    }

    return render(request, 'store/search.html', context)
