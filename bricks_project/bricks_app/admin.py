from django.contrib import admin
from . models import CustomerMaster,VehicleMaster,BillDetails,PaymentMaster
# Register your models here.

admin.site.register(CustomerMaster)
admin.site.register(VehicleMaster)
admin.site.register(BillDetails)
admin.site.register(PaymentMaster)