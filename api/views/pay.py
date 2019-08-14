from django.shortcuts import render
from django.http import JsonResponse
from kombu.utils import json

from db.models import CustomUser
from django.conf import settings
from rest_framework import generics
from db.db_models.pay import *
from api.serializer.pay import OrderInfoSerializer, OrderCheckSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.common.response import *
from alipay import AliPay
from datetime import datetime
from yasuo.config import SITE_DOMAIN
import os
import time
import decimal
from rest_framework import serializers


class AliPayNotifyView(generics.GenericAPIView):
    serializer_class = serializers.Serializer
    permission_classes = (AllowAny,)

    def post(self, request):
        print(time.time())
        print(request.POST)
        order_no = request.POST.get('out_trade_no')
        trade_no = request.POST.get('trade_no')
        trade_status = request.POST.get('trade_status')
        try:
            order = OrderInfo.objects.get(order_no=order_no)
        except:
            return Response('filed')
        order.trade_no = trade_no
        order.trade_status = trade_status
        order.save()

        user_items = CustomUser.objects.get(user=order.payee)
        monery = order.amount / 2
        user_items.credit = user_items.credit + decimal.Decimal(monery)
        user_items.save()
        return Response('success')


# Create your views here.
# ajax post
# 前端传递的参数：订单ID（order_id）
# order/pay
class OrderPayView(generics.GenericAPIView):
    """订单支付"""
    serializer_class = OrderInfoSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # 接受参数
        serializer = OrderInfoSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)

        pay_method = serializer.validated_data.get('pay_method')
        payee = serializer.validated_data.get('payee')
        amount = serializer.validated_data.get('amount')
        pay_item_class = serializer.validated_data.get('pay_item_class')
        pay_item_id = serializer.validated_data.get('pay_item_id')

        # try:
        # 	order = OrderInfo.objects.get(order_id=order_id, user=user, pay_method=2, order_status=1)
        # except OrderInfo.DoesNotExist:
        # 	return JsonResponse({"res": 2, 'errmas': '订单错误'})


        # 业务处理：使用sdk调用支付宝的支付接口
        # 初始化
        app_private_key_string = open(os.path.join(settings.BASE_DIR, "app_private_key.pem")).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, "alipay_public_key.pem")).read()
        alipay = AliPay(
            appid="2019080766140322",
            app_notify_url=SITE_DOMAIN + '/api/order/alipay_notifiy/',
            # app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/blog/app_private_key.pem'),
            app_private_key_string=app_private_key_string,
            # alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/blog/alipay_public_key.pem'),
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",
            debug=False    # 不是调试模式，访问实际环境地址
            # debug=True  # 沙箱开发环境
        )
        user = request.user
        order_no = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        OrderInfo.objects.create(
            order_no=order_no,
            pay_item_id=pay_item_id,
            user=user,
            payee=payee,
            pay_method=pay_method,
            amount=amount,
            pay_item_class=pay_item_class,
            trade_status='WAIT_BUYER_PAY'
        )

        # 调用支付宝接口
        # App支付，将order_string返回给app即可
        order_string = alipay.api_alipay_trade_app_pay(
            out_trade_no=order_no,   # 订单id
            total_amount=str(amount),
            subject='艺起评%s' % order_no,
        )

        # # 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # order_string = alipay.api_alipay_trade_wap_pay(
        # 	out_trade_no=order_id,   #订单id
        # 	total_amount=0.01,
        # 	subject='app 名%s'%order_id,
        # 	return_url=None,
        # 	notify_url=None,   # 可选, 不填则使用默认notify url
        # )

        # 返回应答
        # pay_url = 'https://openapi.alipay.com/gateway.do?' + order_string

        # 沙箱
        # pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

        return json.dumps(order_string, ensure_ascii=False)


# 付款之后紧接调用此函数，查询订单是否完成，给老师钱包增加金额，返回可以读取评论字段
# ajas post
# 前端传递的参数：订单ID（order_id）
# /order/check
class CheckPayView(generics.GenericAPIView):
    """查看订单支付结果"""
    serializer_class = OrderCheckSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """查询支付结果"""

        # 接受参数
        serializer = OrderCheckSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)

        order_no = serializer.validated_data.get('order_no')
        payee = serializer.validated_data.get('payee')

        # 业务处理：使用sdk调用支付宝的支付接口
        # 初始化
        app_private_key_string = open(os.path.join(settings.BASE_DIR, "app_private_key.pem")).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, "alipay_public_key.pem")).read()
        alipay = AliPay(
            appid="2019080766140322",
            app_notify_url=SITE_DOMAIN + '/api/order/alipay_notifiy/',
            # app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/blog/app_private_key.pem'),
            app_private_key_string=app_private_key_string,
            # alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/blog/alipay_public_key.pem'),
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",
            debug=False    # 不是调试模式，访问实际环境地址
            # debug=True    # 沙箱开发环境
        )

        user = request.user
        try:
            order = OrderInfo.objects.get(order_no=order_no, user=user, pay_method=2, trade_status='TRADE_SUCCESS')
        except OrderInfo.DoesNotExist:
            return JsonResponse({"res": 2, 'errmas': '订单错误'})

        # 调用支付宝的交易查询接口
        while True:
            response = alipay.api_alipay_trade_query(order_no)

            # response = {
            # 		"trade_no": "2017032121001004070200176844",  # 支付宝交易号
            # 		"code": "10000",    # 支付宝调用是否成功
            # 		"invoice_amount": "20.00",
            # 		"open_id": "20880072506750308812798160715407",
            # 		"fund_bill_list": [
            # 			{
            # 				"amount": "20.00",
            # 				"fund_channel": "ALIPAYACCOUNT"
            # 			}
            # 		],
            # 		"buyer_logon_id": "csq***@sandbox.com",
            # 		"send_pay_date": "2017-03-21 13:29:17",
            # 		"receipt_amount": "20.00",
            # 		"out_trade_no": "out_trade_no15",
            # 		"buyer_pay_amount": "20.00",
            # 		"buyer_user_id": "2088102169481075",
            # 		"msg": "Success",
            # 		"point_amount": "0.00",
            # 		"trade_status": "TRADE_SUCCESS",    #支付结果
            # 		"total_amount": "20.00"
            # }

            code = response.get('code')
            if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
                """若回调不成功可以使用这个"""
                # 支付成功
                # 获取支付宝交易号
                # 更新支付订单信息
                # trade_no = response.get('trade_no')
                # invoice_amount = request.get('invoice_amount')
                # order.trade_no = trade_no
                # order.order_status = 2
                # order.save()

                # 增加被支付者钱包金额
                # user_items = CustomUser.objects.get(user=payee)
                # user_items.credit = user_items.credit + decimal.Decimal(invoice_amount)
                # user_items.save()

                # 返回结果
                return JsonResponse({'res': 3, 'message': '支付成功'})
            elif code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY':
                # 等待买家付款
                time.sleep(10)
                continue
            else:
                # 支付出错
                return JsonResponse({'res': 4, "message": '支付失败'})


# ajas post
# 前端传递的参数：支付宝账户（payee_account）
# /order/check
class ExtractPayVIew(generics.GenericAPIView):
    """提取账户余额到支付宝"""
    def post(self, request):
        # 用户是否登陆
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmag': '用户未登录'})

        # 业务处理：使用sdk调用支付宝的支付接口
        # 初始化
        app_private_key_string = open("apps/blog/app_private_key.pem").read()
        alipay_public_key_string = open("apps/blog/alipay_public_key.pem").read()

        app_private_key_string == """
                        -----BEGIN RSA PRIVATE KEY-----
                        base64 encoded content
                        -----END RSA PRIVATE KEY-----
                        """

        alipay_public_key_string == """
                        -----BEGIN PUBLIC KEY-----
                        base64 encoded content
                        -----END PUBLIC KEY-----
                        """
        alipay = AliPay(
            appid="2019080766140322",
            app_notify_url=None,
            # app_private_key_path=os.path.join(settings.BASE_DIR, 'apps/blog/app_private_key.pem'),
            app_private_key_path=app_private_key_string,
            # alipay_public_key_path=os.path.join(settings.BASE_DIR, 'apps/blog/alipay_public_key.pem'),
            alipay_public_key_path=alipay_public_key_string,
            sign_type="RSA2",
            debug=False    # 不是调试模式，访问实际环境地址
            # debug=True  # 沙箱开发环境
        )

        # 接受参数
        payee_account = request.POST.get('payee_account')
        amount = request.get('amount')
        # 增加钱包金额
        user = request.user
        # user_items = User.objects.get(user=user)

        if not payee_account or amount:
            return JsonResponse({'res': 1, 'mes': "传入参数有缺失"})
        # 如果取款金额大于钱包余额，报错
        elif amount > user.credit:
            return JsonResponse({'res': 2, 'mes': "传入金额大于钱包余额"})
        else:
            # transfer money to alipay account
            result = alipay.api_alipay_fund_trans_toaccount_transfer(
                datetime.now().strftime("%Y%m%d%H%M%S"),
                payee_type="ALIPAY_LOGONID",
                # payee_account="csqnji8117@sandbox.com",
                payee_account=payee_account,
                amount=3.12
            )

            #返回结果
            # result = {'code': '10000', 'msg': 'Success', 'order_id': '', 'out_biz_no': '', 'pay_date': '2017-06-26 14:36:25'}
            # code = result.get('code')
            # if code == 10000 or code == '10000':
            #     order_id = result.get('order_id')
            #     out_biz_no = result.get('out_biz_no')
            #     pay_date = result.get('pay_date')
            #     return JsonResponse({'code': '10000', 'msg': 'Success', 'order_id': '', 'out_biz_no': '', 'pay_date': '2017-06-26 14:36:25'})
