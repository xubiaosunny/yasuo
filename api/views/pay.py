from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from kombu.utils import json

from db.models import CustomUser, WorksComment, WorksQuestion, Message
from django.conf import settings
from rest_framework import generics
from db.db_models.pay import *
from api.serializer.pay import OrderInfoSerializer, OrderCheckSerializer, TransferInfoSerializer, AliExtractPayNotifySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from utils.common.response import *
from alipay import AliPay
from datetime import datetime
from yasuo.config import SITE_DOMAIN
import os
import time
import decimal
from rest_framework import serializers
from utils.tasks.push import send_push_j
from alipay.compat import urlopen


class MyAliPay(AliPay):
    def api_alipay_fund_trans_toaccount_transfer(
            self, out_biz_no, payee_type, payee_account, amount, payee_real_name, **kwargs):
        assert payee_type in ("ALIPAY_USERID", "ALIPAY_LOGONID"), "unknown payee type"
        biz_content = {
            "out_biz_no": out_biz_no,
            "payee_type": payee_type,
            "payee_account": payee_account,
            "amount": amount,
            "payee_real_name": payee_real_name

        }
        biz_content.update(kwargs)
        data = self.build_body("alipay.fund.trans.toaccount.transfer", biz_content)

        url = self._gateway + "?" + self.sign_data(data)
        raw_string = urlopen(url, timeout=15).read().decode("utf-8")
        return self._verify_and_return_sync_response(
            raw_string, "alipay_fund_trans_toaccount_transfer_response"
        )


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


class AliPayNotifyView(generics.GenericAPIView):
    serializer_class = serializers.Serializer
    permission_classes = (AllowAny,)

    def post(self, request):
        order_no = request.POST.get('out_trade_no')
        trade_no = request.POST.get('trade_no')
        trade_status = request.POST.get('trade_status')
        try:
            order = OrderInfo.objects.get(order_no=order_no)
        except:
            return Response('filed')
        if order.pay_item_class == 'WorksComment':
            works_comment = WorksComment.objects.get(id=order.pay_item_id)
            works_comment.is_pay = True
            works_comment.save()
            user = works_comment.works.user
            send_push_j(works_comment.user_id, '%s收听了您的评论' % (user.full_name or user.phone,),
                        class_name=Message.CLASS_NAME_CHOICES[3][0], class_id=works_comment.id)
        if order.pay_item_class == 'WorksQuestion':
            works_cquestion = WorksQuestion.objects.get(id=order.pay_item_id)
            works_cquestion.is_pay = True
            works_cquestion.save()
            user = works_cquestion.works.user
            send_push_j(works_cquestion.to_id, '%s收听了您的回复' % (user.full_name or user.phone,),
                        class_name=Message.CLASS_NAME_CHOICES[1][0], class_id=works_cquestion.id)
        order.trade_no = trade_no
        order.trade_status = trade_status
        order.save()
        # user_items = CustomUser.objects.get(id=order.payee)
        user_items = order.payee
        monery = order.amount / 2
        user_items.credit += decimal.Decimal(monery)
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
            # app_notify_url=None,
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
            amount=decimal.Decimal(amount),
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
        order_string = json.dumps({"order_string": order_string, "order_no": order_no})
        return HttpResponse(order_string)


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
        # payee = serializer.validated_data.get('payee')

        # 业务处理：使用sdk调用支付宝的支付接口
        # 初始化
        app_private_key_string = open(os.path.join(settings.BASE_DIR, "app_private_key.pem")).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, "alipay_public_key.pem")).read()
        alipay = AliPay(
            appid="2019080766140322",
            # app_notify_url=SITE_DOMAIN + '/api/order/alipay_notifiy/',
            app_notify_url=None,
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
            order = OrderInfo.objects.get(order_no=order_no, user=user, pay_method=2)
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
                # amount = request.get('invoice_amount')
                order.trade_no = request.get('trade_no')
                order.order_status = 'TRADE_SUCCESS'
                order.save()

                # 修改支付的状态，确定可以听评论
                if order.pay_item_class == 'WorksComment':
                    works_comment = WorksComment.objects.get(id=order.pay_item_id)
                    works_comment.is_pay = True
                    works_comment.save()
                if order.pay_item_class == 'WorksQuestion':
                    works_cquestion = WorksQuestion.objects.get(id=order.pay_item_id)
                    works_cquestion.is_pay = True
                    works_cquestion.save()
                # 增加被支付者钱包金额
                user_items = CustomUser.objects.get(user=order.payee)
                monery = order.amount / 2
                user_items.credit += decimal.Decimal(monery)
                user_items.save()
                # 返回结果
                return JsonResponse({'res': 3, 'message': '支付成功'})
                break
            elif code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY':
                # 等待买家付款
                time.sleep(10)
                continue
            else:
                # 支付出错
                return JsonResponse({'res': 4, "message": '支付失败'})
                break


# ajas post
# 前端传递的参数：支付宝账户（payee_account）
# /order/check
class ExtractPayVIew(generics.GenericAPIView):
    """提取账户余额到支付宝"""
    serializer_class = TransferInfoSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # 接收参数
        serializer = TransferInfoSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)

        pay_method = serializer.validated_data.get('pay_method')
        amount = serializer.validated_data.get('amount')
        payee_type = serializer.validated_data.get('payee_type')
        payee_account = serializer.validated_data.get('payee_account')
        payee_real_name = serializer.validated_data.get('payee_real_name')

        # 业务处理：使用sdk调用支付宝的支付接口
        # 初始化
        app_private_key_string = open(os.path.join(settings.BASE_DIR, "app_private_key.pem")).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, "alipay_public_key.pem")).read()
        alipay = AliPay(
            appid="2019080766140322",
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",
            debug=False  # 不是调试模式，访问实际环境地址
        )
        user = request.user
        # if not pay_method or amount or payee_type or payee_account or payee_real_name:
        #     return JsonResponse({'res': 1, 'mes': "传入参数有缺失"})
        # 如果取款金额大于钱包余额，报错
        if amount > user.credit:
            return JsonResponse({'mes': "传入金额大于钱包余额"})
        else:
            out_biz_no = datetime.now().strftime("%Y%m%d%H%M%S")
            TransferInfo.objects.create(
                out_biz_no=out_biz_no,
                payee_account=payee_account,
                payee_type=payee_type,
                pay_method=pay_method,
                payee=user,
                amount=decimal.Decimal(amount),
                # payee_real_name=payee_real_name
            )
            # transfer money to alipay account
            result = alipay.api_alipay_fund_trans_toaccount_transfer(
                # datetime.now().strftime("%Y%m%d%H%M%S"),
                out_biz_no=out_biz_no,
                payee_type=payee_type,
                # payee_account="csqnji8117@sandbox.com",
                payee_account=payee_account,
                amount=str(amount),
                # payee_real_name=payee_real_name
            )
            if result.get('code') == 10000:
                return JsonResponse({'res': 'ok', 'result': result, 'out_biz_no': out_biz_no}, cls=DecimalEncoder)
            else:
                return JsonResponse({"res": result.get("sub_msg")})


class AliExtractPayNotifyView(generics.GenericAPIView):
    """查询转账记录"""
    serializer_class = AliExtractPayNotifySerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        # 接收参数
        serializer = OrderInfoSerializer(data=request.data)
        if not serializer.is_valid():
            return response_400(serializer.errors)
        out_biz_no = serializer.validated_data.get('out_biz_no')
        # 业务处理：使用sdk调用支付宝的支付接口
        # 初始化
        app_private_key_string = open(os.path.join(settings.BASE_DIR, "app_private_key.pem")).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, "alipay_public_key.pem")).read()
        alipay = AliPay(
            appid="2019080766140322",
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",
            debug=False  # 不是调试模式，访问实际环境地址
        )
        # 查询转账结果
        while True:
            result = alipay.api_alipay_fund_trans_order_query(
                out_biz_no=out_biz_no
            )
            print(result)
            if result.get('code') == '10000' and result.get('status') == 'SUCCESS':
                """若回调不成功可以使用这个"""
                # 支付成功
                # 获取支付宝交易号
                # 更新支付订单信息
                notify = TransferInfo.objects.get(out_biz_no=out_biz_no)
                notify.status = result.get('status')
                notify.amount = result.get('order_fee')
                notify.trade_no = result.get('order_id')
                # 扣除用户账户相应余额
                user_items = notify.payee
                user_items.credit -= notify.amount
                user_items.save()
                return Response('success')
            elif result.get('status') == 'INIT' or result.get('status') == 'DEALING':
                # 等待买家付款
                time.sleep(10)
                continue
            else:
                # 支付出错
                return JsonResponse({'res': 4, "message": '支付失败'})


class PayInfo(generics.GenericAPIView):
    """收款记录"""
    serializer_class = serializers.Serializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.user
        payment = OrderInfo.objects.filter(payee=user).all()
        # drawing = TransferInfo.objects.filter(payee=user).all()
        balance = user.credit
        print(user)
        print("yue", balance)
        info_lists = []
        if payment:
            for i in payment:
                info_dict = {}
                payment_user = i.user
                if i.trade_status == 'TRADE_SUCCESS':
                    # info_dict['avatar'] = payment_user.avatar
                    # info_dict['full_name'] = payment_user.full_name
                    # info_dict['city'] = payment_user.city
                    # info_dict['time'] = i.create_time
                    # info_dict['amount'] = i.amount / 2
                    # if payment_user.work_place:
                    #     info_dict['work_place'] = payment_user.work_place
                    # if payment_user.grade:
                    #     info_dict['work_place'] = payment_user.grade
                    # info_lists.append(info_dict)
                    info = payment_user.to_dict()
                    info_dict.update({"user_info": info, "time": i.create_time, "amount": i.amount / 2})
                    info_lists.append(info_dict)
        info_lists = sorted(info_lists, key=lambda x: x["time"], reverse=True)
        data = {
            "data": info_lists,
            "balance": balance
        }
        return JsonResponse(data, safe=False)


class ExtractPayInfo(generics.GenericAPIView):
    """提现记录"""
    serializer_class = AliExtractPayNotifySerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.user
        drawing = TransferInfo.objects.filter(payee=user).all()
        info_lists = []
        if drawing:
            for i in drawing:
                info_dict = {}
                if i.status == 'SUCCESS':
                    info_dict['full_name'] = i.payee.full_name
                    info_dict['time'] = i.create_time
                    info_dict['amount'] = i.amount
                    info_lists.append(info_dict)
        info_lists = sorted(info_lists, key=lambda x: x["time"], reverse=True)
        data = {
            "data": info_lists,
        }
        return JsonResponse(data, safe=False)
