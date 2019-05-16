from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.forms.models import model_to_dict

from api.serializer.auth import LoginSerializer, PhoneSerializer, CertificationSerializer
from utils.common.response import *
from db.models import CustomUser, SMSCode, Certification
from utils.core.sms import CloopenSMS
from utils.common.permissions import SignaturePermission


class SendCodeView(generics.GenericAPIView):
    """
    发送验证码
    """
    serializer_class = PhoneSerializer
    permission_classes = (SignaturePermission,)

    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        phone = serializer.data['phone']
        code_recond = SMSCode.get_last_in_one_minutes(phone)
        if code_recond:
            # Do not repeat sending within one minute
            return response_200({'phone': code_recond.phone, 'send_time': code_recond.send_time})

        code = self._get_random_code()
        sms = CloopenSMS()
        sms.send_code(phone, code)
        code_recond = SMSCode.objects.create(phone=phone, code=code)
        return response_200({'phone': code_recond.phone, 'send_time': code_recond.send_time})

    def _get_random_code(self):
        import random
        code = ''
        for i in range(6):
            code += str(random.randint(0, 9))
        return code


class TokenView(generics.GenericAPIView):
    """
    登陆
    """
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        user, flag = CustomUser.objects.get_or_create(phone=serializer.data['phone'])
        token, flag = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user_info': user.to_dict()
            # 'certification': model_to_dict(user.certification_set) if user.certification_set else None
        }
        return response_200(data)

    def delete(self, request):
        """退出登陆"""
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
        return response_200({})


class CertificationView(generics.GenericAPIView):
    """
    认证信息
    """
    serializer_class = CertificationSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """获取登陆用户（老师）认证信息"""
        try:
            certification = request.user.certification
        except Exception:
            certification = None
        return response_200({'certification': certification.detail()})

    def post(self, request):
        """创建登陆用户（老师）认证信息"""
        serializer = CertificationSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        certification, flag = Certification.objects.update_or_create(
            user=request.user, defaults={'status': Certification.STATUS_CHOICES[0][0], **serializer.validated_data})
        return response_200({'certification': certification.detail()})

    def put(self, request):
        """更新登陆用户（老师）认证信息"""
        serializer = CertificationSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        certification, flag = Certification.objects.update_or_create(
            user=request.user, defaults={'status': Certification.STATUS_CHOICES[0][0], **serializer.validated_data})
        return response_200({'certification': certification.detail()})
