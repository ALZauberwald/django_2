from django.db import models

# L'héritage cré le lien entre la représentation d'une table en python et la table sql en elle meme
class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    # Cette fonction sera surtout utile pour définir ce que renverra linstance de 'objet désiré
    # lorsqu'on l'appelera l'aide de la méthode get dans la console de DJANGO
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Artiste"

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name

    class Meta :
        verbose_name= "prospect"

class Album(models.Model):
    #reference est un entier (IntegerField) null= True --> signifie que le champs est optionnel
    reference = models.IntegerField(null=True)
    # La classe DateTimeField  -->champs de date et heure
    # L'argument auto_now_add=True --> enregistrera automatiquement la date et l'heure du premier enregistrement de l'objet
    created_at= models.DateTimeField(auto_now_add=True)
    # La classe BooleanField prendra True ou False comme valeur
    # (la valeur par defaut est importante si on souhaite plus tard effectuer des recherches par ce filtre)
    available = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    # L'image est un lien vers une image externe contenu sur un autre site donc de type url --> utilisation de la classe URLField
    picture = models.URLField()
    # L'attribut related_name permet d'indiquer le nom à utiliser pour la relation inverse depuis l'objet lié vers celui-ci
    artists = models.ManyToManyField(Artist, related_name='albums', blank=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # Par défaut, les réservations ne sont pas encore traitées
    contacted = models.BooleanField(default=False)
    # Il faut passer en attribu de ForeignKey,la classe du modèle à lier
    # on_delete=models.CASCADE  supprime les réservations faites par un contact si le contact est supprimé
    # mais pas l'inverse
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    # On définit les liens entre les classes(contact avec booking) et (album avec booking) dans Booking car
    # c'est dans cette classe que se trouvent les clez etrangères
    album = models.OneToOneField(Album, on_delete=models.CASCADE)
    # on_delete peut prendre comme valeur :models.CASCADE  models.SET_NULL   models.PROTECT   models.SET_DEFAULT

    def __str__(self):
    # On peut utiliser contact.name car on a lié une instance de la classe Contact dans la variable contact
    #                                                                                 en tant que ForeignKey
    #                                             Et que name est un attribut spécifique de l'instance contact
    #                                             associée
        return self.contact.name

    class Meta:
        verbose_name = "Réservation"
