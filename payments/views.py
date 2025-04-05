import json
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponse

# Home Page
def home(request):
    return render(request, 'payments/index.html')

# User Details View – Displays form and processes input
def user_details(request):
    if request.method == "POST":
        # Retrieve form data from the user details form
        name = request.POST.get("name")
        matric_number = request.POST.get("matric_number")
        registration_number = request.POST.get("registration_number")  # optional
        email = request.POST.get("email")

        # Validate that required fields are provided
        if not (name and matric_number and email):
            error = "Please fill in all required fields (Name, Matric Number, and Email)."
            return render(request, "payments/user_details.html", {"error": error})

        # Store details in the session for later steps
        request.session["user_details"] = {
            "name": name,
            "matric_number": matric_number,
            "registration_number": registration_number,
            "email": email,
        }

        # Redirect to the payment purpose page
        return redirect("payment_purpose")
    
    return render(request, "payments/user_details.html")

# Payment Purpose View – Collects the reason for payment
def payment_purpose(request):
    if request.method == "POST":
        purpose = request.POST.get("purpose")
        if not purpose:
            error = "Please enter the purpose of your payment."
            return render(request, "payments/payment_purpose.html", {"error": error})

        # Store purpose in session
        request.session["payment_purpose"] = purpose

        # Redirect to the payment page
        return redirect("payment_page")

    return render(request, "payments/payment_purpose.html")

# Payment Page View – Displays the payment form to be submitted for Paystack processing
def payment_page(request):
    return render(request, 'payments/payment.html')

# Process Payment View – Sends data to Paystack and redirects to the Paystack payment page
def process_payment(request):
    if request.method == "POST":
        # Retrieve email and amount from the payment form
        email = request.POST.get("email")
        amount = request.POST.get("amount")

        try:
            # Convert amount to kobo (1 Naira = 100 kobo)
            amount_in_kobo = int(amount) * 100
        except ValueError:
            return JsonResponse({"error": "Invalid amount provided."}, status=400)

        # Set up Paystack API endpoint and headers
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": email,
            "amount": amount_in_kobo,
            "callback_url": "http://127.0.0.1:8000/payment-success/",
        }

        # Initialize the transaction with Paystack
        response = requests.post(url, json=data, headers=headers)
        res = response.json()

        if res.get("status") == True:
            # Redirect user to Paystack's authorization URL
            return redirect(res["data"]["authorization_url"])
        else:
            return JsonResponse({"error": "Payment initialization failed. Please try again."}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=400)

# Payment Success View – Displays a success page after payment completion
def payment_success(request):
    return render(request, "payments/payment_success.html")
