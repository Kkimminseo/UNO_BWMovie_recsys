from rest_framework import serializers
from django.contrib.auth import get_user_model

# settings.py에 선언했던 AUTH_USER_MODEL 데려옴
# accounts/models.py.User
User = get_user_model()

class UserRegistartionSerializer(serializers.ModelSerializer):
    # 비밀번호 재확인
    # write_only=True : 필수 요소
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username','nickname', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, attrs):
        # 첫 번째로 입력한 비번이랑 두 번째 입력한 비번이 다르면
        if attrs['password'] != attrs['password2']:
            # 비밀번호가 일치하지 않다는 메시지가 뜨게끔 만들기
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return attrs
    
    def create(self, validated_data):
        
        # validated_data에서 'password2' 키를 제거
        # 'password2'는 비밀번호 확인을 위해 사용되는 필드이기 때문에 저장 안 해도 됨
        validated_data.pop('password2')
        
        # validated_data에서 'password' 키를 제거하고, 그 값을 password 변수에 저장
        # 'password'는 사용자가 입력한 비밀번호이며, 이 값을 사용하여 사용자 객체의 비밀번호를 해싱(암호화)해야 합니다.
        password = validated_data.pop('password')
        
        # validated_data에 남아있는 데이터를 사용하여 User 객체를 생성
        # User 객체는 비밀번호를 제외한 사용자 정보(예: username, email)를 포함
        user = User(**validated_data)
        
        # 사용자 객체의 비밀번호를 설정합니다.
        # set_password() 메서드는 비밀번호를 해싱하고, 해싱된 비밀번호를 사용자 객체에 저장
        user.set_password(password)
        user.save()
        return user