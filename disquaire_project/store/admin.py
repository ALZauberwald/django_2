from django.contrib import admin
# Par convention c'est ici que les réglages de l'interface admin figurent
# Il faut : -d'abord importer les modeles qu'on veut voir apparaitre dans l'interface admin
#           -puis utiliser la methode register

from .models import Album, Artist, Booking, Contact

#admin.site.register(Booking)                      --> méthode rapide mais ne permet pas la customisation
# @admin.register(Booking) + déclaration de classe --> méthode plus lourde mais plus complète

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'contacted'] #permet une recherche par filtre
    readonly_fields = ["created_at"] #champs non modifiable, lecture seule

    #empêche la création de nouvelles instances de réservation dans l'interface admin
    #def has_add_permission(self, request):
    #    return False


class BookingInline(admin.TabularInline):
    #TabularInline indique qu'on veut que les infs s'affichent sur plusieurs lignes en colonnes
    model= Booking
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"
    fieldsets = [ #les champs à afficher
        (None, {'fields': ['album', 'contacted']})
    ]
    extra= 1 # indique si on veut avoir la possibilité de rajouter manuellement des champs et cb

# Le décorateur @admin.register() permet de modifier des parametres dans l'interface admin
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Ci dessous, je précise que je veux voir s'afficher dans contact les lignes contenues dans BookingInline
    # Autrement dit : directement dans contact, je créé une vue sur les réservations(booking) et si "a été contacté" ou non
    inlines = [BookingInline]

#admin.site.register(Artist)

class AlbumArtistInline(admin.TabularInline):
    # Cas d'une relation de plusieurs à plusieurs ( album-artist)
    # "artists" est l'attribut manytomany déclaré dans Album (models.py)
    # "through" va appeler et utiliser la table intermédiaire additionnelle (Album-Artist)créée
    model = Album.artists.through
    verbose_name = "Disque"
    verbose_name_plural = "Disques"
    extra = 1


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistInline]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title'] #ajouter une recherche par mot clez



