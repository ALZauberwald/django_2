# Possibilité 1 pour déclarer son formulaire avec django : forms
# Je la passe en fonction pour garder sa trace ( la possibilité 2 fait la meme chose)
def v1 ():
    from django import forms

    #chaque classe représente un formulaire différent
    #chaque attribut de classe représente un champ du formulaire
    class ContactForm(forms.Form):
        #chaque attribut génerera du html sous forme de <input ...> les attributs renseignés complèteront l'input généré
        # exemple, si on déclare : name = forms.CharField(max_length= 100)
        # etant donné qu'on a spécifié que name etait charfield l'input généré sera sous la forme suivante :
        # <input type="text" name="name" maxlength="100" id="id_name">
        name = forms.CharField(
            label='Nom',
            max_length=100,
            # la classe 'form-control' semble destiné à faire s'effectuer une vérification des entrées renseignée par l'utilisateur
            # lors de la soumission du formulaire (classe html)
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            #required rend le champ à compléter obligatoire pour que le formulaire soit traité
            required=True
        )
        email = forms.EmailField(
            label='Email',
            widget=forms.EmailInput(attrs={'class': 'form-control'}),
            required=True)

# Possibilité 2 pour déclarer son formulaire avec django : ModelForm
# Est plus optimisé que la possibilité 1 car s'adapte en fonction de model

from django.forms import ModelForm, TextInput, EmailInput
from .models import Contact
# La classe ErrorList va servir à customiser le retour des erreurs
from django.forms.utils import ErrorList

#cette classe est créée dans le but de customiser les retours d'erreurs du formulaire
class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    # je dis que je veux que les instances de cette classe renvoient la fonction as_divs que je definis ci dessous

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])
        # renvoi du code en html en forme de paragraphe ( en forme de ligne par defaut)

class ContactForm(ModelForm):
    # Les champs générés par ModelForm  dépendent du contenu de la classe Méta
    class Meta:
        model = Contact # modèle source
        fields = ['name', 'email'] #les champs du model source qu'on veut voir apparaitre dans le formulaire
        #widgets surcharge  les classes prévues par ModelForm.
        # --> doit être un dictionnaire (nom du champ de field : classe ou instance de classe
        widgets={
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}) #'class': 'form-control' --> definit une classe html
        }
        # se lit : Le champ est déclaré de type text/mail et de class html form-control
        # implique que si ce n'est pas le cas, la soumission ne se fait pas  et form.errors.items() complété
        # (on recupere les erreurs dans views.py puis on les transmet dans le gabarit pour informer utilisateur)


