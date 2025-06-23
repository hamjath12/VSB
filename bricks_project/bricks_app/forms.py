from django import forms
from . models import CustomerMaster, PaymentMaster,VehicleMaster,BillDetails

class AddCustomerForm(forms.ModelForm):
    Customer_Name = forms.CharField(label='Name', max_length=100, required=True)
    Customer_Phone = forms.CharField(label='Phone Number', max_length=20, required=True)
    Customer_Address = forms.CharField(label='Address', max_length=100, required=True)

    class Meta:
        model = CustomerMaster
        exclude = ['Customer_Id', 'Customer_Status', 'Paid_Amount', 'Pending_Amount', 'Bill_Amount']


class AddVehicleForm(forms.ModelForm):
    Vehicle_Registration_No=forms.CharField(label='Vehicle Register Number',max_length=20,required=True)

    class Meta:
        model=VehicleMaster
        exclude=['Vehicle_Id','Vehicle_Status']


class AddBillDetailsForm(forms.ModelForm):
    Customers_Details = forms.CharField(
        label="Customer Details",
        required=True,
        error_messages={"required": "Customer Details is required."}
    )

    Vehicle_Details = forms.CharField(
        label="Vehicle Details",
        required=True,
        error_messages={"required": "Vehicle Details is required."}
    )

    class Meta:
        model = BillDetails
        exclude = [
            'Bill_Status',
            'Customer_Id', 'Customer_Name', 'Customer_Phone', 'Customer_Address',
            'Vehicle_Id', 'Vehicle_Registration_No'
        ]
        error_messages = {
            'Trip_Date': {'required': "Trip Date is required."},
            'Destination': {'required': "Destination is required."},
            'Driver_Name': {'required': "Driver Name is required."},
            'Quantity': {'required': "Quantity is required."},
            'Bill_Amount': {'required': "Bill Amount is required."},
            'Rate_Per_Bricks': {'required': "Rate Per Bricks is required."},
        }

    def clean_Customers_Details(self):
        value = self.cleaned_data.get('Customers_Details')
        try:
            customer_id, customer_name, customer_phone, customer_address = [x.strip() for x in value.split('---')]
        except ValueError:
            raise forms.ValidationError("Invalid format. Use: ID --- Name --- Phone --- Address")

        self.cleaned_data['Customer_Id'] = customer_id
        self.cleaned_data['Customer_Name'] = customer_name
        self.cleaned_data['Customer_Phone'] = customer_phone
        self.cleaned_data['Customer_Address'] = customer_address
        return value

    def clean_Vehicle_Details(self):
        value = self.cleaned_data.get('Vehicle_Details')
        try:
            vehicle_id, registration_no = [x.strip() for x in value.split('---')]
        except ValueError:
            raise forms.ValidationError("Invalid format. Use: Vehicle ID --- Registration No")

        self.cleaned_data['Vehicle_Id'] = vehicle_id
        self.cleaned_data['Vehicle_Registration_No'] = registration_no
        return value

    def clean(self):
        cleaned_data = super().clean()

        try:
            quantity = float(cleaned_data.get("Quantity", "0"))
            if quantity <= 0:
                self.add_error("Quantity", "Quantity must be greater than 0.")
        except ValueError:
            self.add_error("Quantity", "Enter a valid number.")

        try:
            amount = float(cleaned_data.get("Bill_Amount", "0"))
            if amount <= 0:
                self.add_error("Bill_Amount", "Bill Amount must be greater than 0.")
        except ValueError:
            self.add_error("Bill_Amount", "Enter a valid number.")

        try:
            rate = float(cleaned_data.get("Rate_Per_Bricks", "0"))
            if rate <= 0:
                self.add_error("Rate_Per_Bricks", "Rate Per Bricks must be greater than 0.")
        except ValueError:
            self.add_error("Rate_Per_Bricks", "Rate Per Bricks must be a valid number.")

        return cleaned_data







class AddPaymentForm(forms.ModelForm):
    Customer_Details = forms.CharField(
        label="Customer Details",
        required=True,
        error_messages={"required": "Customer Details is required."}
    )

    class Meta:
        model = PaymentMaster
        exclude = ['Payment_Id', 'Payment_Date']
        widgets = {
            'Pay_Amount': forms.NumberInput(attrs={'placeholder': 'Enter Pay Amount'}),
            'Description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_Customer_Details(self):
        value = self.cleaned_data['Customer_Details']
        try:
            bill_id, name, destination = [x.strip() for x in value.split('---')]
        except ValueError:
            raise forms.ValidationError("Invalid format. Use: Bill ID --- Name --- Destination")

        self.cleaned_data['Bill_Id'] = bill_id
        self.cleaned_data['Customer_Name'] = name
        self.cleaned_data['Destination'] = destination
        return value

class AddPaymentForm(forms.ModelForm):
    class Meta:
        model = PaymentMaster
        fields = ['Pay_Amount']
        widgets = {
            'Pay_Amount': forms.NumberInput(attrs={
                'class': 'form-control border-success shadow-sm',
                'placeholder': 'Enter Amount',
                'step': '0.01',
                'min': '0',
                'required': True,  # HTML-level validation
            }),
        }

