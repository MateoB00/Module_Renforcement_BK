from rest_framework import viewsets, permissions
from .models import Auteur, Livre, Categorie, Exemplaire, Emprunt, Commentaire, Editeur, Evaluation, OTP
from .serializers import (
    AuteurSerializer,
    LivreSerializer,
    CategorieSerializer,
    ExemplaireSerializer,
    EmpruntSerializer,
    CommentaireSerializer,
    EditeurSerializer,
    EvaluationSerializer, 
    CustomTokenObtainPairSerializer,
)
from .paginations import AuteurPagination, LivrePagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import views, status
from rest_framework.response import Response
from django.core.mail import send_mail
import random
import string
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            otp_code = ''.join(random.choices(string.digits, k=6))
            OTP.objects.create(user=user, code=otp_code)

            email = MIMEText(f'OTP Code : {otp_code}')
            email['Subject'] = "OTP Code"
            email['From'] = os.getenv('email')
            email['To'] = user.email
            
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                    smtp_server.login(os.getenv('email'), os.getenv('password'))
                    smtp_server.sendmail(os.getenv('email'), user.email, email.as_string())  # `user.email` au lieu de `email['To']`

                return Response({"detail": "OTP envoyé à votre e-mail"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": f"Une erreur s'est produite lors de l'envoi de l'e-mail : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "Identifiants incorrects"}, status=status.HTTP_401_UNAUTHORIZED)

class ValidateOTPView(views.APIView):
    def post(self, request):
        username = request.data.get('username')
        otp_code = request.data.get('otp')

        try:
            user = User.objects.get(username=username)
            otp_record = OTP.objects.filter(user=user, code=otp_code, is_used=False).first()

            if otp_record and otp_record.is_valid():
                otp_record.is_used = True
                otp_record.save()

                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)

            return Response({"detail": "OTP invalide ou expiré"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)

class ResendOTPView(views.APIView):
    def post(self, request):
        username = request.data.get('username')

        try:
            user = User.objects.get(username=username)
            otp_code = ''.join(random.choices(string.digits, k=6))
            OTP.objects.create(user=user, code=otp_code)

            email = MIMEText(f'OTP Resend Code : {otp_code}')
            email['Subject'] = "OTP Resend Code"
            email['From'] = os.getenv('email')
            email['To'] = user.email
            
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                    smtp_server.login(os.getenv('email'), os.getenv('password'))
                    smtp_server.sendmail(os.getenv('email'), user.email, email.as_string()) 

                return Response({"detail": "OTP envoyé à votre e-mail"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"detail": f"Une erreur s'est produite lors de l'envoi de l'e-mail : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable"}, status=status.HTTP_404_NOT_FOUND)

class AuteurViewSet(viewsets.ModelViewSet):
    queryset = Auteur.objects.all()
    serializer_class = AuteurSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = AuteurPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["date_de_naissance"]
    search_fields = ["nom", "biographie"]
    ordering_fields = ['nom', 'date_de_naissance']
    ordering = ['date_de_naissance'] 

class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = LivrePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["titre"]
    search_fields = ["isbn"]
    ordering_fields = ['date_de_publication', 'editeur']
    ordering = ['date_de_publication'] 

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class ExemplaireViewSet(viewsets.ModelViewSet):
    queryset = Exemplaire.objects.all()
    serializer_class = ExemplaireSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class EmpruntViewSet(viewsets.ModelViewSet):
    queryset = Emprunt.objects.all()
    serializer_class = EmpruntSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class EditeurViewSet(viewsets.ModelViewSet):
    queryset = Editeur.objects.all()
    serializer_class = EditeurSerializer
    permission_classes = [permissions.IsAuthenticated]

class EvaluationViewSet(viewsets.ModelViewSet):
    queryset = Evaluation.objects.all()
    serializer_class = EvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]
