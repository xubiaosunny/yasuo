from rest_framework import generics

from api.serializer.auth import LoginSerializer, PhoneSerializer
from shared.common.response import *
from db.models import CustomUser, SMSCode
from shared.core.sms import CloopenSMS


class SendCodeView(generics.CreateAPIView):
    serializer_class = PhoneSerializer

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


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        return response_200(None)
