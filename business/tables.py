#!/usr/bin/env python
# coding: utf-8

import django

if django.VERSION >= (1, 10):
    from django.urls import reverse_lazy
else:
    from django.core.urlresolvers import reverse_lazy

from table.columns import Column
from table.columns.calendarcolumn import CalendarColumn
from table.columns.sequencecolumn import SequenceColumn
from table.columns.imagecolumn import ImageColumn
from table.columns.linkcolumn import LinkColumn, Link, ImageLink
from table.columns.checkboxcolumn import CheckboxColumn

from table import Table
from .models import *

class AjaxSourceTable(Table):
    id = Column(field = 'bulk_id')
    bulk_title = Column(field = 'bulk_title')
    reseller_name = Column(field = 'reseller_name')
    reseller_mob = Column(field = 'reseller_mob')
    bulk_receive_mode = Column(field = 'bulk_receive_mode')
    start_time = Column(field = 'start_time')
    dead_time = Column(field = 'dead_time')
    bulk_status = Column(field = 'bulk_status')
    countsize = Column(field = 'countsize')
    details = Column(field = 'bulk_id')
    class Meta:
        model = BulkDetails
        ajax = True
        ajax_source = reverse_lazy('ajax_source_api')


class OrderTable(Table):
    order_id = Column(field = 'order_id')
    user_id = Column(field = 'user_id')
    receive_mode = Column(field = 'receive_mode')
    total_fee = Column(field = 'total_fee')
    status = Column(field = 'status')
    pay_status = Column(field = 'pay_status')
    third_party_fee = Column(field = 'third_party_fee')
    balance_fee = Column(field = 'balance_fee')
    third_party_order_id = Column(field = 'third_party_order_id')
    create_time = Column(field = 'create_time')
    product = Column(field = 'product')
    location = Column(field = 'location')
    obtain_name = Column(field = 'obtain_name')
    obtain_mob = Column(field = 'obtain_mob')
    receive_address = Column(field = 'receive_address')
    receive_name = Column(field = 'receive_name')
    receive_mob = Column(field = 'receive_mob')
    comments = Column(field = 'comments') 
    id = Column()
    class Meta:
	model = OrderDetails	
	ajax = True
	ajax_source = reverse_lazy('ajax_order_api')

    
