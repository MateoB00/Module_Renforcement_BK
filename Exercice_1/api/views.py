from rest_framework import viewsets, permissions
from .models import Auteur, Livre, Categorie, Exemplaire, Emprunt, Commentaire, Editeur, Evaluation
from .serializers import (
    AuteurSerializer,
    LivreSerializer,
    CategorieSerializer,
    ExemplaireSerializer,
    EmpruntSerializer,
    CommentaireSerializer,
    EditeurSerializer,
    EvaluationSerializer
)
from .paginations import AuteurPagination, LivrePagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = AuteurPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["date_de_naissance"]
    search_fields = ["nom", "biographie"]
    ordering_fields = ['nom', 'date_de_naissance']
    ordering = ['date_de_naissance'] 

class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = LivrePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]g
    filterset_fields = ["titre"]
    search_fields = ["isbn"]
    ordering_fields = ['date_de_publication', 'editeur']
    ordering = ['date_de_publication'] 

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
