from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from .models import User

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user with role-based profile creation
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authenticate user and return token
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout user and delete token
    """
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({
            'error': 'Token not found'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get current user profile
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    """
    Get role-specific dashboard data
    """
    user = request.user
    
    if user.role == 'doctor':
        return Response({
            'role': 'doctor',
            'welcome_message': f'Welcome Dr. {user.first_name} {user.last_name}',
            'stats': {
                'total_patients': 45,
                'appointments_today': 8,
                'pending_consultations': 3
            }
        })
    elif user.role == 'patient':
        return Response({
            'role': 'patient',
            'welcome_message': f'Welcome {user.first_name} {user.last_name}',
            'stats': {
                'upcoming_appointments': 2,
                'medical_records': 12,
                'prescriptions': 3
            }
        })
    elif user.role == 'nurse':
        return Response({
            'role': 'nurse',
            'welcome_message': f'Welcome Nurse {user.first_name} {user.last_name}',
            'stats': {
                'patients_assigned': 15,
                'tasks_pending': 7,
                'shift_hours': 8
            }
        })
    else:
        return Response({
            'error': 'Invalid role'
        }, status=status.HTTP_400_BAD_REQUEST)