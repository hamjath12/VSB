import base64
import datetime
import io
import json
from django.http import JsonResponse
from django.shortcuts import render ,redirect
import qrcode
from . models import CustomerMaster,VehicleMaster,BillDetails,PaymentMaster
from . forms import AddCustomerForm,AddVehicleForm,AddBillDetailsForm,AddPaymentForm
from datetime import date
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Sum

def dashboard(request):
      return render(request,'index.html')

def add_customer(request):
    form=AddCustomerForm()
    last_customer = CustomerMaster.objects.order_by('-Customer_Id').first()
    if last_customer:
        last_id = int(last_customer.Customer_Id[4:])  # Extract the numeric part
        new_id = f"CUST{last_id + 1:04d}"         
    else:
        new_id = "CUST0001"

    if request.method=='POST':
        form=AddCustomerForm(request.POST)
        print("data sent Post forms.py")
        if form.is_valid():
            print("data valid")
            customer = CustomerMaster()
            customer.Customer_Id = new_id
            customer.Customer_Status = 1
            customer.Customer_Name = form.cleaned_data['Customer_Name']
            customer.Customer_Phone = form.cleaned_data['Customer_Phone']
            customer.Customer_Address = form.cleaned_data['Customer_Address']
            customer.save()
            print("data saved success")
            messages.success(request,"Add customer successfully")
            return redirect('add_customer')

    return render(request,"add_customer.html",{'form':form,'new_id':new_id})
       
def list_customer(request):
    customer_data=CustomerMaster.objects.filter(Customer_Status=1)
    return render(request,'list_customer.html',{'customer_data':customer_data})
       
       
def edit_customer(request,Customer_Id):
    user=get_object_or_404(CustomerMaster,Customer_Id=Customer_Id)
    if request.method=="POST":
        form=AddCustomerForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request," customer Edited successfully")
            return redirect('list_customer')
    else:
        form=AddCustomerForm(instance=user)
    return render(request,'edit_customer.html',{'user':user})

def delete_customer(request,Customer_Id):
    user=get_object_or_404(CustomerMaster,Customer_Id=Customer_Id)
    user.Customer_Status=0
    user.save()
    messages.success(request," customer Deleted successfully")
    return redirect('list_customer')


def add_vehicle(request):
    form=AddVehicleForm()
    last_customer = VehicleMaster.objects.order_by('-Vehicle_Id').first()
    if last_customer:
        last_id = int(last_customer.Vehicle_Id[4:])  # Extract the numeric part
        new_id = f"VEHI{last_id + 1:04d}"         
    else:
        new_id = "VEHI0001"
    if request.method=="POST":
        form=AddVehicleForm(request.POST)
        if form.is_valid():
            print("data valid")
            vehicle_no = form.cleaned_data['Vehicle_Registration_No'].upper()

            if VehicleMaster.objects.filter(Vehicle_Registration_No=vehicle_no).exists():
                messages.error(request,"this vehicle number already exists")
                return render(request, "add_vehicle.html",{'new_id':new_id,'form':form})
            else:
                vehicle=form.save(commit=False)
                vehicle.Vehicle_Id=new_id
                vehicle.Vehicle_Registration_No=vehicle_no
                vehicle.Vehicle_Status=1
                vehicle.save()
                print("data saved success")
                messages.success(request,"Add Vehicle successfully")
                return redirect('add_vehicle')  
    return render(request, "add_vehicle.html",{'new_id':new_id,'form':form})

def list_vehicle(request):
    list_vehicle=VehicleMaster.objects.filter(Vehicle_Status=1)
    return render(request,"list_vehicle.html",{'list_vehicle':list_vehicle})

def edit_vehicle(request,Vehicle_Id):
    vehicle_detail=get_object_or_404(VehicleMaster,Vehicle_Id=Vehicle_Id)
    form=AddCustomerForm(instance=vehicle_detail)

    if request.method=='POST':
        form=AddVehicleForm(request.POST,instance=vehicle_detail)
        if form.is_valid():
            form.save()
            print("data saved success")
            messages.success(request," Vehicle Edited successfully")
            return redirect('list_vehicle')
        
    return render(request,"edit_vehicle.html",{'vehicle_detail':vehicle_detail,'form':form})

def delete_vehicle(request,Vehicle_Id):
    vehicle_detail=get_object_or_404(VehicleMaster,Vehicle_Id=Vehicle_Id)
    vehicle_detail.Vehicle_Status=0
    vehicle_detail.Vehicle_Status
    vehicle_detail.save()
    print("data saved success")
    messages.success(request," Vehicle Deleted successfully")
    return redirect('list_vehicle')


def add_bill(request):
    # Generate new bill ID
    last_bill = BillDetails.objects.order_by('-Bill_Id').first()

    if last_bill:
        last_id = int(last_bill.Bill_Id[4:])
        new_id = f"BILL{last_id + 1:04d}"
    else:
        new_id = "BILL0001"

    if request.method == "POST":
        form = AddBillDetailsForm(request.POST)
        if form.is_valid():
            bill_obj = form.save(commit=False)
            bill_obj.Bill_Id = new_id
            bill_obj.Bill_Status = 1  # active

            # Assign parsed customer details
            bill_obj.Customer_Id = form.cleaned_data['Customer_Id']
            bill_obj.Customer_Name = form.cleaned_data['Customer_Name']
            bill_obj.Customer_Phone = form.cleaned_data['Customer_Phone']
            bill_obj.Customer_Address = form.cleaned_data['Customer_Address']

            # Assign parsed vehicle details
            bill_obj.Vehicle_Id = form.cleaned_data['Vehicle_Id']
            bill_obj.Vehicle_Registration_No = form.cleaned_data['Vehicle_Registration_No']

            bill_obj.save()

            try:
                customer = CustomerMaster.objects.get(Customer_Id=bill_obj.Customer_Id)
                customer.Bill_Amount += bill_obj.Bill_Amount or 0
                customer.Pending_Amount = customer.Bill_Amount - customer.Paid_Amount
                customer.save()
            except CustomerMaster.DoesNotExist:
                messages.warning(request, "Warning: Customer not found in CustomerMaster table.")

            messages.success(request, "Bill added successfully.")
            return redirect('add_bill')
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = AddBillDetailsForm()

    vehicle_data = VehicleMaster.objects.filter(Vehicle_Status=1)
    customer_data = CustomerMaster.objects.filter(Customer_Status=1)
    today = date.today().strftime('%Y-%m-%d') 


    return render(request, 'add_bill3.html', {
        'form': form,
        'new_id': new_id,
        'vehicle_data': vehicle_data,
        'sent': customer_data,
        'today': today,
    })




def list_bill(request):
    part=BillDetails.objects.filter(Bill_Status=1)
    context={'sent':part}
    return render(request,'list_bill.html',context)



def add_payment(request, Customer_Id):
    customer = get_object_or_404(CustomerMaster, Customer_Id=Customer_Id)

    if not customer.Bill_Amount or customer.Bill_Amount == 0:
        messages.error(request, "This customer has no bill. Cannot accept payment.")
        return redirect('list_customer')  # or any other page you prefer
    
    # Get all trip bills for this customer
    trip_data = BillDetails.objects.filter(Customer_Id=Customer_Id)
    total_bill = trip_data.aggregate(total=Sum('Bill_Amount'))['total'] or 0
    total_paid = customer.Paid_Amount or 0
    pending_amount = total_bill - total_paid

    # Generate new Payment ID
    last_payment = PaymentMaster.objects.order_by('-Payment_Id').first()
    if last_payment:
        last_id = int(last_payment.Payment_Id[4:])
        new_id = f"PAY{last_id + 1:04d}"
    else:
        new_id = "PAY0001"

    if request.method == 'POST':
        
        form = AddPaymentForm(request.POST)
        if form.is_valid():
                pay_amount = form.cleaned_data.get('Pay_Amount') or 0.0  # fallback if None

                if pay_amount <= 0:
                    messages.error(request, "Pay amount must be greater than 0.")
                    return redirect(request.path)
                
                if pay_amount > pending_amount:
                    messages.error(request, f"Pay amount ({pay_amount}) cannot exceed pending amount ({pending_amount}).")
                    return redirect(request.path)


                payment = PaymentMaster.objects.create(
                    Payment_Id=new_id,
                    Customer_Id=customer.Customer_Id,
                    Customer_Name=customer.Customer_Name,
                    Customer_Phone=customer.Customer_Phone,
                    Customer_Address=customer.Customer_Address,
                    Pay_Amount=pay_amount,
                    Payment_Date=date.today(),
                    Bill_Amount=customer.Bill_Amount,
                    Paid_Amount=customer.Paid_Amount + pay_amount,
                    Pending_Amount=customer.Bill_Amount - (customer.Paid_Amount + pay_amount)
                )

                # Update Customer record
                customer.Paid_Amount += pay_amount
                customer.Pending_Amount = customer.Bill_Amount - customer.Paid_Amount
                customer.save()
                messages.success(request, f"Payment added successfully {customer.Customer_Name}")

                return redirect('list_customer')
    else:
        # 💡 Initial form with default 0 or blank, not 0.0
        form = AddPaymentForm(initial={'Pay_Amount': ''})

    context = {
        'form': form,
        'customer': customer,
        'new_id': new_id,
        'total_bill': total_bill,
        'pending_amount': pending_amount,
    }
    return render(request, 'add_payment.html', context)




def list_payment(request):
    part=PaymentMaster.objects.filter(Payment_Status=1)
    context={'sent':part}
    return render(request,'list_payment.html',context)








# def addPayments(request,id):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)  # Load request data once
#             table_data = data.get("tableData", [])
#             last_pay = Payment_Master.objects.filter(Payment_Id__startswith=id).order_by('-Payment_Id').first()  

#             if last_pay:        
#                 last_id = int(last_pay.Payment_Id[13:])  # Extract the numeric part
#                 new_pay_id = f"{id}-{last_id + 1:02d}"
#             else:
#                 new_pay_id = f"{id}"

#             customer = bill_details.objects.get(bill_id = id.split("-")[0])

#             customer_id = customer.customer_id
#             customer_name = customer.customer_name
#             phone_no = customer.phone
            
                



#             paym_id = Payment_Master.objects.create(
#                 Payment_Id=new_pay_id,
#                 Bill_Id = id.split("-")[0],
#                 Grand_Total=int(float(data.get("totalAmount") or 0)),  # Ensure it's never None
#                 Paid_Amount=int(float((data.get("totalAmount") or 0)) - int(float((data.get("finalPending") or 0)))),
#                 Pending_Amount=int(float(data.get("finalPending") or 0)), 
#                 Added_By = request.user.username
                
#             )

#             bill_details.objects.filter(bill_id = id.split("-")[0]).update(
#                 Fully_Paid=1 if data.get("finalPending") == "0.00" else 0,  # Fully paid if no pending amount
#                 Partialy_Paid=1 if 0 < int(float((data.get("finalPending") or 0))) < int(float((data.get("totalAmount") or 0))) else 0,  # Partial payment
#                 Not_Paid=1 if (data.get("totalAmount") or 0) == (data.get("finalPending") or 0) else 0,  # Not paid if pending = total
#                 paid_amount = int(float(data.get("totalAmount"))) - int(float(data.get("finalPending"))),
#                 pending_amount = int(float(data.get("finalPending")))
#                 )
                
#             for entry in table_data:
#                 Payment_Details.objects.create(
#                     Payment_Id=paym_id,
#                     Customer_Id = customer_id,
#                     Customer_Name = customer_name,
#                     Phone_Number = phone_no,
#                     Grand_Total=int(float(data.get("totalAmount") or 0)),  # Ensure it's never None
#                     Paid_Amount=int(float(entry.get("amount"))),  # Avoid NoneType subtraction
#                     Pending_Amount=int(float(entry.get("pending_amount") or 0)),   # Ensure correct pending amount
#                     Payment_Mode=entry.get("payment_mode"),
#                     Utr_Or_Reason="N/A",
#                     Mobile_No=entry.get("mobile_number"),
#                     Bill_Id = id.split("-")[0],
#                     Added_By = request.user.username
                    
#                 )
#                 if entry.get("payment_mode") == "MANUAL CLOSE":
#                     bill_details.objects.filter(bill_id = id.split("-")[0]).update(
#                     Force_Paid=1 if entry.get("payment_mode") == "MANUAL CLOSE" else 0,  # Set Force_Paid if MANUAL_CLOSE
#                     )


#             return JsonResponse({"message": "Data received successfully"}, status=200)


#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON data"}, status=400)  # Use 400 for bad requests
        
    
     

#     last_pay = Payment_Master.objects.filter(Payment_Id__startswith=id).order_by('-Payment_Id').first() 
#     if last_pay:
#         last_id = int(last_pay.Payment_Id[12:])  # Extract the numeric part
#         new_pay_id = f"{id}-PAY{last_id + 1:02d}"
#         data=bill_details.objects.get(bill_id = id, status = 1)
#     else:
#         new_pay_id = f"{id}-PAY01"
#         data=bill_details.objects.get(bill_id = id, status = 1)
    
#     context = {'data': data,'new_pay_id' : new_pay_id,'bill_id':id}
    
#     return render(request,'add_payments2.html',context)



# def overall_invoice(request,id):
    
#     data = bill_details.objects.filter(bill_id = id , status =1)
#     data2 = bill_details.objects.get(bill_id = id , status =1)
   
#     data3 = customer_details.objects.get(customer_id = data2.customer_id)
  
#     data4 = bill_details.objects.filter(bill_id=id)
#     data5 = Payment_Details.objects.filter(Bill_Id=id)
#     current_date = data2.date

#     upi_id = "sudheerk1462@okicici"

#     if data4:
#         for item in data4:
#             amount = item.pending_amount
#     else:
#         amount = data2.Bill_Amount

#     upi_link = f"upi://pay?pa={upi_id}&pn=Payee&am={amount}&cu=INR"

#     # Generate QR code
#     qr = qrcode.QRCode(box_size=10, border=4)
#     qr.add_data(upi_link)
#     qr.make(fit=True)
    
#     # Convert QR to image
#     img = qr.make_image(fill="black", back_color="white").resize((400, 400))

#     # Convert image to Base64 to embed in HTML
#     buffer = io.BytesIO()
#     img.save(buffer, format="PNG")
#     qr_base64 = base64.b64encode(buffer.getvalue()).decode()

#     context = {'data':data, 'data2':data2,'data3':data3,'current_date':current_date,'data4':data4,'billId':id,'invoice_no':id,'data5':data5,'qr_base64': qr_base64}
#     return render(request,'overall_invoice.html',context)


# def bill_payment_details(request,id):
#     data = bill_details.objects.filter(bill_id = id , status =1)
#     data2 = bill_details.objects.get(bill_id = id , status =1)
#     data3= Payment_Master.objects.filter(Payment_Id__startswith=id)
#     context = {'data':data, 'data2':data2, 'data3':data3,'id':id}
#     # return render(request,'bill_details.html',context) 
#     return render(request,'list_bill_payments.html',context)


