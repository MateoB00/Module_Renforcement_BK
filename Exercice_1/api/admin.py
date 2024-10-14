from django.contrib import admin
from api import models

admin.site.register(models.Auteur)
admin.site.register(models.Livre)
admin.site.register(models.Categorie)
admin.site.register(models.Exemplaire)
admin.site.register(models.Emprunt)
admin.site.register(models.Commentaire)
admin.site.register(models.Editeur)
admin.site.register(models.Evaluation)

