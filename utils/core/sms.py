import hashlib
import requests
import datetime
import base64

from yasuo.config import SMS_CLOOPEN


class CloopenStatusCodeException(Exception):
    pass


class CloopenSMS():
    def __init__(self):
        self.account_sid = SMS_CLOOPEN['accountSid']
        self.account_token = SMS_CLOOPEN['accountToken']
        self.app_id = SMS_CLOOPEN['appId']
        self.server_ip = SMS_CLOOPEN['serverIP']
        self.server_port = int(SMS_CLOOPEN['serverPort'])
        self.soft_version = SMS_CLOOPEN['softVersion']

    def _get_sig_parameter(self, time_str):
        signature = self.account_sid + self.account_token + time_str
        md5 = hashlib.md5()
        md5.update(signature.encode('utf-8'))
        return md5.hexdigest().upper()

    def _get_hesders(self, time_str):
        src = '%s:%s' % (self.account_sid, time_str)
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            # 'Content-Length': '256',
            'Authorization': base64.encodebytes(src.encode('utf-8')).strip()
        }
        return headers

    def _send_sms(self, template_id, to_list, datas):
        params = {
            "to": ','.join(to_list),
            "appId": self.app_id,
            "templateId": str(template_id),
            "datas": datas,
        }

        time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        headers = self._get_hesders(time_str)
        sig_parameter = self._get_sig_parameter(time_str)
        url = 'https://%s:%d/%s/Accounts/%s/SMS/TemplateSMS?sig=%s' % (self.server_ip, self.server_port,
                                                                       self.soft_version, self.account_sid,
                                                                       sig_parameter)
        req = requests.post(url, json=params, headers=headers)
        return req.json()

    def send_code(self, phone, code):
        res = self._send_sms(SMS_CLOOPEN.get('verification_code_template_id'), [phone], [code, '5'])
        if res['statusCode'] != '000000':
            raise CloopenStatusCodeException('%s:%s' % (res['statusCode'], res['statusMsg']))


