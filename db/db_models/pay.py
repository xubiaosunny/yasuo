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
    amount = models.DecimalField(max_digits=10, decimal_places=3, verbose_name='价格')
    trade_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='支付状态')
    pay_item_class = models.CharField(choices=PAY_ITEM_CLASS_CHOICES, verbose_name="所支付类名")
    pay_item_id = models.IntegerField(verbose_name='所支付的id')
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True, blank=True)
    uodate_time = models.DateTimeField(_('Update Time'), auto_now=True, blank=True)

    def __str__(self):
        return self.order_id
