from rest_framework import viewsets, permissions
from .models import Auteur, Categorie, Exemplaire, Emprunt, Commentaire, Editeur, Evaluation
from .serializers import (
    AuteurSerializer,
    CategorieSerializer,
    ExemplaireSerializer,
    EmpruntSerializer,
    CommentaireSerializer,
    EditeurSerializer,
    EvaluationSerializer
)

class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ExemplaireViewSet(viewsets.ModelViewSet):
    queryset = Exemplaire.objects.all()
    serializer_class = ExemplaireSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EmpruntViewSet(viewsets.ModelViewSet):
    queryset = Emprunt.objects.all()
    serializer_class = EmpruntSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EditeurViewSet(viewsets.ModelViewSet):
    queryset = Editeur.objects.all()
    serializer_class = EditeurSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
