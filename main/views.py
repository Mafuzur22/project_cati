from django.shortcuts import render, redirect
from main.sslcommerz import sslcommerz_payment_gateway
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string, get_template
from django.conf import settings
from weasyprint import HTML
from django.core.mail import EmailMessage
from django.contrib import messages
import os
from io import BytesIO
import uuid


# Create your views here.
def home(request):
  return render(request, 'base.html')
  
def donate(request):
  return render(request, 'donate.html')
  
def payment(request):
  if request.method == "POST":
    data = request.POST
    name = data.get('name')
    usr_email = data.get('email')
    amount = data.get('amount')
    address = data.get('address')
    address = str(address)
    if int(amount) <= 0:
      messages.error(request, "Please Donate more then 0BDT!")
      return redirect("/donate")
    
    return redirect(sslcommerz_payment_gateway(request, name, amount, usr_email, address))
    
  return redirect("/")
  
@csrf_exempt
def donation_done(request):
    if request.method == 'POST':
        data = request.POST    
        
        # Extract data from form
        name = data.get('value_a')
        usr_email = data.get('value_b')
        amount = data.get('amount')
        address = data.get('value_c')

        # Prepare the context for the template
        #context = {
        #    'name': name,
        #    'description': description,
        #}
        iv_number = uuid.uuid4()
        iv_number = str(iv_number)
        context = {
              'invoice_number': 'INV-'+iv_number,
              'donation_date': '2024-09-19',
              'donor_name': name,
              'donor_email': usr_email,
              'donor_address': address,
              'donation_type': 'One-time Donation',
              'donation_description': 'Supporting Cats in need.',
              'donation_amount': amount,
              'organization_name': 'Charity Organization',
              'organization_address': '123 Charity Lane, Dhaka, Bangladesh',
              'organization_contact': 'info@charity.org, +8801765432112',
        }

        # Render the HTML template with context
        #html_content = render_to_string('main/pdf_template.html', context)
        fetch_temp = get_template('invoice_template.html')
        html_content = fetch_temp.render(context)
        pdf_file = BytesIO()
        pdf_file_name = f'{iv_number}.pdf'
        pdf_file_path = os.path.join(settings.BASE_DIR, 'pdfs', pdf_file_name)

        # Convert the HTML content to PDF
        #os.makedirs(os.path.dirname(pdf_file_path))
        pdf = HTML(string=html_content).write_pdf(target=pdf_file_path)
        HTML(string=html_content).write_pdf(pdf_file)
        pdf_file.seek(0)
        #Send Email
        subject = "Donation Invoice."
        from_email = settings.EMAIL_HOST_USER
        recipient = [usr_email]
        
        email = EmailMessage(
          subject = subject,
          body = html_content,
          from_email = from_email,
          to = recipient,
          )
        email.content_subtype = "html"
        email.attach(f'DonationInvoice{iv_number}.pdf', pdf_file.read() ,'application/pdf') 
        email.send()
        context = {
          "email": usr_email,
        }
        return render(request, 'donation_done.html', context)

      
    return redirect("/")
    