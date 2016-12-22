#!/usr/bin/env python
# coding: utf-8

from django.shortcuts import render

# Create your views here.

from .models import *
from table.views import FeedDataView
from business.tables import (
    AjaxSourceTable,OrderTable
)

from django.db.models import Q
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import(
        AllowAny,
        IsAuthenticated
)
from rest_framework.decorators import(
        api_view,
        permission_classes,
        parser_classes,
)

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from django import forms
from django.views.decorators.csrf import csrf_exempt


@login_required
def login_home_pag(request):
    
    return render(request,'batchlist.html')

@login_required
def login_order_details(request):
    
    return render(request,'batchdetails.html')

@login_required
def login_order_list(request):

    return render(request,'order.html')

def ceshi(request):
   
   return render(request,'ceshi.html')

def location(request):

   return render(request,'location.html')


class MyDataView(FeedDataView):

    token = AjaxSourceTable.token

    def get_queryset(self):

        id = self.request.GET['filter[batch_id]']
        name = self.request.GET['filter[batch_name]']
        mob = self.request.GET['filter[batch_mob]']
        status = self.request.GET['fileter[batch_status]']

        queryset = super(MyDataView, self).get_queryset()

        if id:
            queryset = queryset.filter(bulk_id = id)
        if name:
            queryset = queryset.filter(bulk_title__contains = name)
        if mob:
            queryset = queryset.filter(reseller_mob__contains = mob)
        if status:
            queryset = queryset.filter(bulk_status = status)

	return queryset


class OrderDataView(FeedDataView):
    
    token = OrderTable.token

    def convert_queryset_to_values_list(self, queryset):
	data = []
	for obj in queryset:
		row = []
		for col in self.columns:
			if col.field is not None:
				val = getattr(obj, col.field)
				if val is None:
					row.append('')
				else:
					row.append(col.render(obj))
			else:
				row.append(col.render(obj))
		data.append(row)
	return data

    def get_queryset(self):
	
	bulk_id = self.request.GET['filter[batch_id]']
        number = self.request.GET['filter[order_number]']
        mob = self.request.GET['filter[order_mob]']
        status = self.request.GET['filter[pay_status]']
        start_time = self.request.GET['filter[start_day]']
        end_time = self.request.GET['filter[end_day]']
	
        queryset = super(OrderDataView,self).get_queryset()

        if bulk_id:
            queryset = queryset.filter(bulk_id = bulk_id)
        if number:
            queryset = queryset.filter(order__id__contains = number)
        if mob:
            queryset = queryset.filter(Q(obtain_mob__contains = mob)|Q(receive_mob__contains = mob))
        if status:
            queryset = queryset.filter(status = status)
	
        if start_time and end_time:
            queryset = queryset.filter(create_time__range = (start_time,end_time))

        return queryset


@api_view(['GET'])
@permission_classes([AllowAny])
def bulks(request):

    bulk_list = []
    bulk_id = request.GET.get('filter[batch_id]',None)
    print bulk_id
    bulks = BulkDetails.objects.filter(bulk_id = bulk_id)
    for x in bulks:
        bulk_id = x.bulk_id
	reseller_name = x.reseller_name
	bulk_title = x.bulk_title
	reseller_mob = x.reseller_mob
	bulk_receive_mode = x.bulk_receive_mode
        bulk_start_time = x.start_time
	bulk_status = x.bulk_status
	countsize = x.countsize
        bulk_dead_time = x.dead_time

        bulk_data ={
           'bulk_id':bulk_id,
	   'bulk_title':bulk_title,
	   'reseller_mob':reseller_mob,
	   'bulk_receive_mode':bulk_receive_mode,
	   'bulk_status':bulk_status,
	   'countsize':countsize,
	   'reseller_name':reseller_name,
           'start_time':bulk_start_time,
           'dead_time':bulk_dead_time
        }
        bulk_list.append(bulk_data)
    rst_data = {
        "data":bulk_list
    }

    return Response(rst_data,status=status.HTTP_200_OK)	


