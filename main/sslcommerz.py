from sslcommerz_lib import SSLCOMMERZ

def sslcommerz_payment_gateway(request, name, amount, usr_email, address):


    store_auth = {'store_id': 'mfsof66ed859fde60f',
            'store_pass': 'mfsof66ed859fde60f@ssl', 'issandbox': True}

    sslcommez = SSLCOMMERZ(store_auth)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = 1234
    post_body['success_url'] = 'https://mafuzur22.pythonanywhere.com/donationok'
    post_body['fail_url'] = 'http://donatehub.herokuapp.com/payment/faild/'
    post_body['cancel_url'] = 'http://donatehub.herokuapp.com/'
    post_body['emi_option'] = 0
    post_body['cus_name'] = name
    post_body['cus_email'] = usr_email
    post_body['cus_phone'] = 'request.data["phone"]'
    post_body['cus_add1'] = 'request.data["address"]'
    post_body['cus_city'] = 'request.data["address"]'
    post_body['cus_country'] = 'Bangladesh'
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"

    # OPTIONAL PARAMETERS
    post_body['value_a'] = name
    post_body['value_b'] = usr_email
    post_body['value_c'] = address

    response = sslcommez.createSession(post_body)
    return 'https://sandbox.sslcommerz.com/gwprocess/v4/gw.php?Q=pay&SESSIONKEY=' + response["sessionkey"]