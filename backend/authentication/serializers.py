from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, DoctorProfile, PatientProfile, NurseProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 
                 'last_name', 'role', 'phone_number', 'date_of_birth', 'address']
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        
        # Create profile based on role
        try:
            if user.role == 'doctor':
                DoctorProfile.objects.create(
                    user=user,
                    license_number=f"DOC{user.id:06d}",  # Generate a default license number
                    specialization="General Medicine"  # Default specialization
                )
            elif user.role == 'patient':
                PatientProfile.objects.create(
                    user=user, 
                    patient_id=f"P{user.id:04d}",
                    emergency_contact="",  # Will be filled later
                    blood_type=""  # Will be filled later
                )
            elif user.role == 'nurse':
                NurseProfile.objects.create(
                    user=user, 
                    nurse_id=f"N{user.id:04d}",
                    department="General",  # Default department
                    shift="Day"  # Default shift
                )
        except Exception as e:
            # If profile creation fails, delete the user to maintain consistency
            user.delete()
            raise serializers.ValidationError(f"Failed to create profile: {str(e)}")
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User account is disabled")
            else:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Must provide username and password")
        
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 
                 'phone_number', 'date_of_birth', 'address', 'created_at']