from django.db import models


class CustomerMaster(models.Model):
    Customer_Id = models.CharField(max_length=20, unique=True)
    Customer_Name = models.CharField(max_length=100)
    Customer_Phone = models.BigIntegerField()
    Customer_Address = models.CharField(max_length=200)

    Paid_Amount = models.FloatField(default=0, blank=True)
    Pending_Amount = models.FloatField(default=0, blank=True)
    Bill_Amount = models.FloatField(default=0, blank=True)
    
    Customer_Status = models.IntegerField(default=1)

    def __str__(self):
        return self.Customer_Name

    
class VehicleMaster(models.Model):
    Vehicle_Id=models.CharField(max_length=20)
    Vehicle_Registration_No=models.CharField(max_length=20,null=True)
    Vehicle_Status=models.IntegerField(default=1)

    def __str__(self):
        return self.Vehicle_Registration_No
    


class BillDetails(models.Model):
    #customer details
    Customer_Id=models.CharField(max_length=20)
    Customer_Name=models.CharField(max_length=255)
    Customer_Phone=models.BigIntegerField()
    Customer_Address=models.CharField(max_length=200)
    Trip_Date = models.DateField(null=True, auto_now=False, auto_now_add=False)
    Destination=models.CharField(max_length=200)
    Driver_Name=models.CharField(max_length=100)
    Vehicle_Id=models.CharField(max_length=20)
    Vehicle_Registration_No=models.CharField(max_length=20,null=True)
    #bill details
    Bill_Id = models.CharField(max_length=50,primary_key=True)
    Quantity = models.FloatField(null=True, max_length=50)
    Bill_Amount = models.FloatField(null=True, max_length=50)
    Rate_Per_Bricks = models.FloatField(max_length=50,null=True)
    Bill_Status=models.IntegerField(default=1)

    def __str__(self):
        return self.Customer_Name
    


class PaymentMaster(models.Model):
    Payment_Id = models.CharField(max_length=50, primary_key=True)
    Customer_Id = models.CharField(max_length=20)
    Customer_Name = models.CharField(max_length=100)
    Customer_Phone = models.BigIntegerField()
    Customer_Address = models.CharField(max_length=200)
    Payment_Date = models.DateField(auto_now_add=True)
    Pay_Amount = models.FloatField(default=0.0)

    Paid_Amount = models.FloatField(default=0, blank=True)
    Pending_Amount = models.FloatField(default=0, blank=True)
    Bill_Amount = models.FloatField(default=0, blank=True)
    Payment_Status=models.IntegerField(default=1)


    def __str__(self):
        return self.Customer_Name







# class Payment_Master(models.Model):
#     Payment_Id = models.CharField(max_length=50,primary_key=True)
#     Bill_Id = models.CharField(default="BILL0001", max_length=50)
#     Grand_Total = models.IntegerField(default=0)
#     Paid_Amount = models.IntegerField(default=0)
#     Pending_Amount = models.IntegerField(default=0)
#     Added_By = models.CharField(null=True, max_length=50)
#     Date = models.DateField(null=True, auto_now=False, auto_now_add=True)


# class Payment_Details(models.Model):
#     Payment_Id = models.ForeignKey("bricks_app.Payment_Master", on_delete=models.CASCADE)
#     Customer_Id = models.CharField(null=True, max_length=50)
#     Customer_Name = models.CharField(null=True, max_length=50)
#     Phone_Number = models.BigIntegerField(null=True)
#     Grand_Total = models.IntegerField(default=0)
#     Payment_Date = models.DateField(auto_now=True,auto_now_add=False)
#     Paid_Amount = models.IntegerField(default=0)
#     Pending_Amount = models.IntegerField(default=0)
#     Payment_Mode = models.CharField(max_length=50)
#     Utr_Or_Reason = models.CharField(max_length=50)
#     Mobile_No = models.CharField(max_length=50)
#     Bill_Id = models.CharField(default="BILL0001", max_length=50)
#     Added_By = models.CharField(null=True, max_length=50)
#     Date = models.DateField(null=True, auto_now=False, auto_now_add=True)
