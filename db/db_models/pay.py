from django.db import models
from django.utils import timezone
from decimal import Decimal

from django.utils.translation import gettext as _


class OrderInfo(models.Model):
    ORDER_STATUS_CHOICES = (
        ('WAIT_BUYER_PAY', '交易创建，等待买家付款'),
        ('TRADE_CLOSED', '在指定时间段内未支付时关闭的交易；在交易完成全额退款成功时关闭的交易。'),
        ('TRADE_SUCCESS', '交易成功，且可对该交易做操作，如：多级分润、退款等'),
        ('TRADE_FINISHED', '交易成功且结束，即不可再做任何操作。')
    )
    PAY_METHOD_CHOICES = (
        (1, '微信支付'),
        (2, '支付宝支付')
    )
    PAY_ITEM_CLASS_CHOICES = (
        ('WorksComment', '作品评论'),
        ('WorksQuestion', '作品提问')
    )

    trade_no = models.CharField(max_length=64, verbose_name='支付宝交易号')
    order_no = models.CharField(max_length=64, verbose_name='传入支付宝id')
    user = models.ForeignKey('CustomUser', verbose_name='付款方', on_delete=models.PROTECT)
    payee = models.ForeignKey('CustomUser', related_name='order_payee', verbose_name='收款方', on_delete=models.PROTECT)
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name="支付方式")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    trade_status = models.CharField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='支付状态', max_length=50)
    pay_item_class = models.CharField(max_length=50, choices=PAY_ITEM_CLASS_CHOICES, verbose_name="所支付类名")
    pay_item_id = models.IntegerField(verbose_name='所支付的id')
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True, blank=True)
    uodate_time = models.DateTimeField(_('Update Time'), auto_now=True, blank=True)


class TransferInfo(models.Model):
    PAY_TYPE_CHOICES = (
        ('ALIPAY_USERID', '支付宝账号对应的支付宝唯一用户号。以2088开头的16位纯数字组成'),
        ('ALIPAY_LOGONID', '支付宝登录号，支持邮箱和手机号格式')
    )
    PAY_METHOD_CHOICES = (
        (1, '微信支付'),
        (2, '支付宝支付')
    )
    trade_no = models.CharField(max_length=64, verbose_name='支付宝交易号')
    out_biz_no = models.CharField(max_length=64, verbose_name='商户转账唯一订单号')
    payee_account = models.CharField(max_length=64, verbose_name='支付宝账户')
    payee_real_name = models.CharField(max_length=64,  verbose_name='收款方姓名')
    payee_type = models.CharField(choices=PAY_TYPE_CHOICES, default=1, verbose_name='收款方账户类型', max_length=50)
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name="支付方式")
    status = models.CharField(verbose_name='支付状态', max_length=64)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='转账金额')
    payee = models.ForeignKey('CustomUser', related_name='transfer_payee', verbose_name='收款方', on_delete=models.PROTECT)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True, blank=True)
    uodate_time = models.DateTimeField(_('Update Time'), auto_now=True, blank=True)
