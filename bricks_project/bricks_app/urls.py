from django.urls import path
from . import views


urlpatterns=[ 
    path('', views.dashboard, name='dashboard'),

    path('add_customer/', views.add_customer, name='add_customer'),
    path('list_customer/',views.list_customer, name='list_customer'),
    path('edit_customer/<str:Customer_Id>',views.edit_customer, name='edit_customer'),
    path('delete_customer/<str:Customer_Id>',views.delete_customer, name='delete_customer'),

    path('add_vehicle/',views.add_vehicle, name='add_vehicle'),
    path('list_vehicle/',views.list_vehicle, name='list_vehicle'),
    path('edit_vehicle/<str:Vehicle_Id>',views.edit_vehicle, name='edit_vehicle'),
    path('delete_vehicle/<str:Vehicle_Id>',views.delete_vehicle, name='delete_vehicle'),

    path('add_bill/',views.add_bill,name='add_bill'),
    path('list_bill/',views.list_bill,name='list_bill'),
    path('add_payment/<str:Customer_Id>',views.add_payment,name='add_payment'),
    path('list_payment/',views.list_payment, name='list_payment'),


    # path('addpayment/<str:id>/',views.addPayments,name='addpayment'),
    # path('overallinvoice/<str:id>/',views.overall_invoice,name='overallinvoice'),
    # path('listbillpayments/<str:id>/',views.bill_payment_details,name='listbillpayments'),
]