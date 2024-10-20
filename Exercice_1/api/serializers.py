from rest_framework import serializers
from .models import Auteur, Livre, Categorie, Exemplaire, Emprunt, Commentaire, Editeur, Evaluation
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if user is None:
            raise serializers.ValidationError('Invalid credentials')

        token = self.get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return {
            'access': str(token.access_token),
            'refresh': str(token),
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auteur
        fields = ['id', 'nom', 'biographie', 'date_de_naissance', 'date_de_deces', 'nationalite', 'photo']

    def validate_nom(self, value):
        if not value:
            raise serializers.ValidationError("Le nom de l'auteur ne peut pas être vide.")
        if len(value) > 255:  
            raise serializers.ValidationError("Le nom de l'auteur ne peut pas dépasser 255 caractères.")
        return value

    def validate_nationalite(self, value):
        if not value:
            raise serializers.ValidationError("La nationalité de l'auteur ne peut pas être vide.")
        if len(value) > 100: 
            raise serializers.ValidationError("La nationalité de l'auteur ne peut pas dépasser 100 caractères.")
        return value

class LivreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livre
        fields = ['id', 'titre', 'resume', 'date_de_publication', 'isbn', 'nombre_de_pages', 'langue', 'image_de_couverture', 'editeur', 'format']

    def validate_titre(self, value):
        if not value:
            raise serializers.ValidationError("Le titre ne peut pas être vide.")
        if len(value) > 255:
            raise serializers.ValidationError("Le titre ne peut pas dépasser 255 caractères.")
        return value

    def validate_resume(self, value):
        if not value:
            raise serializers.ValidationError("Le résumé ne peut pas être vide.")
        return value

    def validate_isbn(self, value):
        if not value:
            raise serializers.ValidationError("Le numéro ISBN ne peut pas être vide.")
        if len(value) != 13:
            raise serializers.ValidationError("Le numéro ISBN doit comporter exactement 13 caractères.")
        if not value.isdigit():
            raise serializers.ValidationError("Le numéro ISBN doit contenir uniquement des chiffres.")
        return value

    def validate_nombre_de_pages(self, value):
        if not value:
            raise serializers.ValidationError("Le nombre de pages ne peut être vide")
        if value <= 0:
            raise serializers.ValidationError("Le nombre de pages doit être supérieur à zéro.")
        return value

    def validate_langue(self, value):
        if not value:
            raise serializers.ValidationError("La langue ne peut pas être vide.")
        if len(value) > 50:
            raise serializers.ValidationError("La langue ne peut pas dépasser 50 caractères.")
        return value

    def validate_format(self, value):
        if not value:
            raise serializers.ValidationError("Le format ne peut être vide")
        return value

    def validate_image_de_couverture(self, value):
        if value:
            max_size = 2 * 1024 * 1024
            if value.size > max_size:
                raise serializers.ValidationError("L'image de couverture ne peut pas dépasser 2MB.")
            valid_mime_types = ['image/jpeg', 'image/png']
            if value.content_type not in valid_mime_types:
                raise serializers.ValidationError("L'image de couverture doit être au format JPEG ou PNG.")
        return value

    def validate_editeur(self, value):
        if not Editeur.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Éditeur invalide.")
        return value

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'description', 'slug']

    def validate_nom(self, value):
        if not value:
            raise serializers.ValidationError("Le nom de la catégorie ne peut pas être vide.")
        if len(value) > 255:
            raise serializers.ValidationError("Le nom de la catégorie ne peut pas dépasser 255 caractères.")
        return value

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("La description de la catégorie ne peut pas être vide.")
        return value

class ExemplaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exemplaire
        fields = ['id', 'livre', 'etat', 'date_acquisition', 'localisation', 'disponibilite']

    def validate_etat(self, value):
        if not value:
            raise serializers.ValidationError("L'état de l'exemplaire ne peut pas être vide.")
        if len(value) > 50:
            raise serializers.ValidationError("L'état de l'exemplaire ne peut pas dépasser 50 caractères.")
        return value

    def validate_localisation(self, value):
        if not value:
            raise serializers.ValidationError("La localisation de l'exemplaire ne peut pas être vide.")
        if len(value) > 255:
            raise serializers.ValidationError("La localisation de l'exemplaire ne peut pas dépasser 255 caractères.")
        return value

class EmpruntSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprunt
        fields = ['id', 'exemplaire', 'user', 'date_emprunt', 'date_retour_prevue', 'date_retour_effective', 'statut', 'remarques']

    def validate_date_retour_prevue(self, value):
        from datetime import datetime
        if value < datetime.now():
            raise serializers.ValidationError("La date de retour prévue ne peut pas être dans le passé.")
        return value

    def validate_date_retour_effective(self, value):
        if value is not None and value < self.instance.date_emprunt:
            raise serializers.ValidationError("La date de retour effective ne peut pas être antérieure à la date d'emprunt.")
        return value

    def validate_statut(self, value):
        valid_status = ['En cours', 'Terminé', 'En retard']
        if value not in valid_status:
            raise serializers.ValidationError(f"Le statut doit être l'un des suivants : {', '.join(valid_status)}.")
        return value

    def validate(self, data):
        date_retour_prevue = data.get('date_retour_prevue')
        date_retour_effective = data.get('date_retour_effective')
        if date_retour_effective and date_retour_effective < date_retour_prevue:
            raise serializers.ValidationError("La date de retour effective ne peut pas être antérieure à la date de retour prévue.")
        return data

class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ['id', 'livre', 'user', 'contenu', 'date_publication', 'note', 'visible', 'modere']

    def validate_contenu(self, value):
        if not value:
            raise serializers.ValidationError("Le contenu du commentaire ne peut pas être vide.")
        return value

    def validate_note(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La note doit être comprise entre 1 et 5.")
        return value

class EditeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editeur
        fields = ['id', 'nom', 'adresse', 'site_web', 'email_contact', 'description', 'logo']

    def validate_nom(self, value):
        if not value:
            raise serializers.ValidationError("Le nom de l'éditeur ne peut pas être vide.")
        return value

    def validate_adresse(self, value):
        if not value:
            raise serializers.ValidationError("L'adresse ne peut pas être vide.")
        return value

    def validate_site_web(self, value):
        if not value:
            raise serializers.ValidationError("L'URL du site web doit être valide.")
        return value

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id', 'user', 'livre', 'note', 'commentaire', 'date_evaluation', 'recommande', 'titre']

    def validate_titre(self, value):
        if not value:
            raise serializers.ValidationError("Le titre de l'évaluation ne peut pas être vide.")
        if len(value) > 255:
            raise serializers.ValidationError("Le titre ne peut pas dépasser 255 caractères.")
        return value

    def validate_note(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La note doit être comprise entre 1 et 5.")
        return value