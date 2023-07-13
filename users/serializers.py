from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator

from django.contrib.auth.password_validation import validate_password   

from dj_rest_auth.serializers import TokenSerializer

class RegisterSerializer(serializers.ModelSerializer):
    
    #! Normalde email ile dj-rest-auth paketi sayesinde password kullanarak login yapabiliyoruz. Ancak email başta unique olmadığından  tekrar tanımlayıp unique true yapıyoruz. Bu sayede registiration esnasında zorunlu alan oluyor ve bunu kullanıp sisteme giriş yapabiliyoruz. 
    
    email = serializers.EmailField(                        
        required = True, 
        validators = [UniqueValidator(queryset=User.objects.all())] )

    password = serializers.CharField(
        write_only=True,        #! write-only demek yalnızca paswordü gir, dönüşte bana geri getirme. GET ile alınamaz.
        required =True,
        validators=[validate_password],   #settings.py veya base.py'daki password_validatorslere göre işlem yapıyor. 
        style ={"input_type":"password"}
        )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style ={"input_type":"password"}
        )
    
# normalde User içerisinde (databasede password2 yok. Password2 yi diğer tüm data ile birlikte önce kullanıcıdan alacağız. Sonra password ile match edip kullanıcıyı database'e kaydetmeden önce tekrar validated-datadan çıakracağız )
    class Meta:                                  
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2',]
    
        # extra_kwargs ={           #! yukarıda belirtmediysem burada da ekstra ayar belirtebilirim.
        #     'password': {'write_only': True},
        #     'password2': {'write_only': True},
        # }

    # def validate_last_name(self, value):    #! bu şekilde yalnız bir field ile ilgili validate yapılabilir. 

    # bu validate func ile passwordleri match edip doğruluyoruz. Eğer doğruysa User içerisinde yer alan aşağıdaki create metodunu override edip yeni user oluşturuyoruz. 
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
                )

        return attrs

    def create(self, validated_data):
        password = validated_data.get("password")
        validated_data.pop("password2")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")
    
     
class CustomTokenSerializer(TokenSerializer):
    user = UserTokenSerializer(read_only = True)
    
    class Meta(TokenSerializer.Meta):
        fields = ("key", "user")
        

    
