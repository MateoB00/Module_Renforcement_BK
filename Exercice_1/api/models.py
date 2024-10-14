from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Auteur(models.Model):
    nom = models.CharField(max_length=255)
    biographie = models.TextField()
    date_de_naissance = models.DateField()
    date_de_deces = models.DateField(null=True, blank=True)
    nationalite = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='auteurs_photos/', null=True, blank=True)

    def __str__(self):
        return self.nom


class Livre(models.Model):
    titre = models.CharField(max_length=255)
    resume = models.TextField()
    date_de_publication = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    nombre_de_pages = models.PositiveIntegerField()
    langue = models.CharField(max_length=50)
    image_de_couverture = models.ImageField(upload_to='livres_couvertures/', null=True, blank=True)
    # editeur = models.CharField(max_length=255) 
    editeur = models.ForeignKey('Editeur', related_name='livres', on_delete=models.CASCADE)
    format = models.CharField(max_length=50)

    def __str__(self):
        return self.titre


class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nom


class Exemplaire(models.Model):
    livre = models.ForeignKey(Livre, related_name='exemplaires', on_delete=models.CASCADE)
    etat = models.CharField(max_length=50)
    date_acquisition = models.DateField()
    localisation = models.CharField(max_length=255)
    disponibilite = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.livre.titre} - {self.localisation}"


class Emprunt(models.Model):
    exemplaire = models.ForeignKey(Exemplaire, related_name='emprunts', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='emprunts', on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour_prevue = models.DateTimeField()
    date_retour_effective = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=50, choices=[('En cours', 'En cours'), ('Terminé', 'Terminé'), ('En retard', 'En retard')])
    remarques = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} a emprunté {self.exemplaire}"


class Commentaire(models.Model):
    livre = models.ForeignKey(Livre, related_name='commentaires', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='commentaires', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    note = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    visible = models.BooleanField(default=True)
    modere = models.BooleanField(default=False)

    def __str__(self):
        return f"Commentaire de {self.user.username} sur {self.livre.titre}"


class Editeur(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    site_web = models.URLField(null=True, blank=True)
    email_contact = models.EmailField(null=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='editeurs_logos/', null=True, blank=True)

    def __str__(self):
        return self.nom


class Evaluation(models.Model):
    user = models.ForeignKey(User, related_name='evaluations', on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, related_name='evaluations', on_delete=models.CASCADE)
    note = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) 
    commentaire = models.TextField(blank=True)
    date_evaluation = models.DateTimeField(auto_now_add=True)
    recommande = models.BooleanField(default=False)
    titre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} a noté {self.livre.titre} à {self.note}/5"
