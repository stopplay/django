from users.models import Address, User, Establishment
import requests
import json
from datetime import date, datetime, timedelta
from users.models import User, Establishment, Address, Order
import http.client
import json
import requests
from datetime import date, timedelta


# Validate the address of the user 
def validate_user_address(user):
   check_address = user.address
   print(check_address)

   url = f"https://api.sandbox.stuart.com/v2/addresses/validate?address={check_address}&type=picking&phone=07890655555"
   payload = "{}"

   headers = {
    'Authorization': 'Bearer eyJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJzdHVhcnQtYXBpIiwiaWF0IjoxNjQzNzM4Njk3LCJqdGkiOiJlZjg3MDYzMC0yNDZlLTQ1ZjgtOWE1Ni1hNjFhNTMwZDNlODEiLCJzcnQ6ZW52aXJvbm1lbnRzIjpbInNhbmRib3giXSwic3J0OmNsaWVudF9pZCI6IjQ0OTgzOSIsInNydDpjbGllbnRfaWRzIjpbIjQ0OTgzOSJdLCJzcnQ6em9uZV9jb2RlcyI6WyJhbnkiXSwic3J0OmZsZWV0X2lkcyI6WyIxIl0sInNydDpxdWVyaWVzIjpbIl9fc2NoZW1hIiwiX190eXBlbmFtZSIsIndob2FtaSIsInBhY2thZ2UiLCJwYWNrYWdlcyIsInpvbmVzIl0sInNydDptdXRhdGlvbnMiOlsicGFja2FnZSJdfQ.ywxA0s1alyYTKmpgCKNIlce9kiDbUBIunedhBdKOiDR3kTVEaJkJGRfKt3iO5qUpuPv08mfkgIBIRkVqHvmw1A',
    'Content-Type': 'application/json'
    }

   response = requests.request("GET", url, data=payload, headers=headers)
   json_response = response.json() 
   valid_address = json_response
   results = valid_address.get('success', [])
   return(results)

#validate the address of the establishment
def validate_establishments_address(establishment):
   check_address = establishment.address
   print()
   print(check_address)

   url = f"https://api.sandbox.stuart.com/v2/addresses/validate?address={check_address}&type=picking&phone=07890655555"
   payload = "{}"

   headers = {
    'Authorization': 'Bearer eyJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJzdHVhcnQtYXBpIiwiaWF0IjoxNjQzNzM4Njk3LCJqdGkiOiJlZjg3MDYzMC0yNDZlLTQ1ZjgtOWE1Ni1hNjFhNTMwZDNlODEiLCJzcnQ6ZW52aXJvbm1lbnRzIjpbInNhbmRib3giXSwic3J0OmNsaWVudF9pZCI6IjQ0OTgzOSIsInNydDpjbGllbnRfaWRzIjpbIjQ0OTgzOSJdLCJzcnQ6em9uZV9jb2RlcyI6WyJhbnkiXSwic3J0OmZsZWV0X2lkcyI6WyIxIl0sInNydDpxdWVyaWVzIjpbIl9fc2NoZW1hIiwiX190eXBlbmFtZSIsIndob2FtaSIsInBhY2thZ2UiLCJwYWNrYWdlcyIsInpvbmVzIl0sInNydDptdXRhdGlvbnMiOlsicGFja2FnZSJdfQ.ywxA0s1alyYTKmpgCKNIlce9kiDbUBIunedhBdKOiDR3kTVEaJkJGRfKt3iO5qUpuPv08mfkgIBIRkVqHvmw1A',
    'Content-Type': 'application/json'
    }

   response = requests.request("GET", url, data=payload, headers=headers)
   json_response = response.json() 
   valid_address = json_response
   results = valid_address.get('success', [])
   return(results)
   

def post_stuart_price(order):
    e_profile = order.establishment
    u_profile = order.user
    print(e_profile.address)

    # Get price
    url2 = "https://api.sandbox.stuart.com/v2/jobs/pricing"

    payload = json.dumps({ 
        "job": {
        "assignment_code": "JIMMY",
        "pickup_at" : "2022-02-03T16:00:00.000+01:00",
        "pickups": [
        {
            "address": str(e_profile.address),
            "comment": order.comment,
            "pickup_at": "13:00",
            "contact": {
            "firstname": e_profile.name,
            "lastname": e_profile.surname,
            "phone": e_profile.phone,
            "email": e_profile.email,
            "company": e_profile.companyname,
            }
        }
        ],
        "dropoffs": [
        {
            "package_type": "small",
            "package_description": "",
            "address": str(u_profile.address),
            "comment": "",
            "contact": {
            "firstname": u_profile.name,
            "lastname": u_profile.surname,
            "phone": u_profile.phone,
            "email": u_profile.email,
            "company": ""
            }
        }]
        }
    })

    headers = {
    'Authorization': 'Bearer eyJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJzdHVhcnQtYXBpIiwiaWF0IjoxNjQzNzM4Njk3LCJqdGkiOiJlZjg3MDYzMC0yNDZlLTQ1ZjgtOWE1Ni1hNjFhNTMwZDNlODEiLCJzcnQ6ZW52aXJvbm1lbnRzIjpbInNhbmRib3giXSwic3J0OmNsaWVudF9pZCI6IjQ0OTgzOSIsInNydDpjbGllbnRfaWRzIjpbIjQ0OTgzOSJdLCJzcnQ6em9uZV9jb2RlcyI6WyJhbnkiXSwic3J0OmZsZWV0X2lkcyI6WyIxIl0sInNydDpxdWVyaWVzIjpbIl9fc2NoZW1hIiwiX190eXBlbmFtZSIsIndob2FtaSIsInBhY2thZ2UiLCJwYWNrYWdlcyIsInpvbmVzIl0sInNydDptdXRhdGlvbnMiOlsicGFja2FnZSJdfQ.ywxA0s1alyYTKmpgCKNIlce9kiDbUBIunedhBdKOiDR3kTVEaJkJGRfKt3iO5qUpuPv08mfkgIBIRkVqHvmw1A',
    'Content-Type': 'application/json'
    }

    # stuart_order = json_response.get("pricing")
    
    response = requests.request("POST", url2, headers=headers, data=payload)
    json_response = response.json()
    stuart_price = json_response
    estimated_price = stuart_price.get('amount',[])
    print(estimated_price)
    order.stuart_delivery_fee =+ estimated_price
    order.save()
    return json_response


def post_stuart_job(order):
    e_profile = order.establishment
    u_profile = order.user
    print(e_profile.address)

    # Get price
    url = "https://api.sandbox.stuart.com/v2/jobs/"

    payload = json.dumps({ 
        "job": {
        "assignment_code": "JIMMY",
        "pickup_at" : "2022-02-03T16:00:00.000+01:00",
        "pickups": [
        {
            "address": str(e_profile.address),
            "comment": order.comment,
            "pickup_at": "13:00",
            "contact": {
            "firstname": e_profile.name,
            "lastname": e_profile.surname,
            "phone": e_profile.phone,
            "email": e_profile.email,
            "company": e_profile.companyname,
            }
        }
        ],
        "dropoffs": [
        {
            "package_type": "small",
            "package_description": "",
            "address": str(u_profile.address),
            "comment": "",
            "contact": {
            "firstname": u_profile.name,
            "lastname": u_profile.surname,
            "phone": u_profile.phone,
            "email": u_profile.email,
            "company": ""
            }
        }]
        }
    })

    headers = {
    'Authorization': 'Bearer eyJhbGciOiJFUzI1NiJ9.eyJpc3MiOiJzdHVhcnQtYXBpIiwiaWF0IjoxNjQzNzM4Njk3LCJqdGkiOiJlZjg3MDYzMC0yNDZlLTQ1ZjgtOWE1Ni1hNjFhNTMwZDNlODEiLCJzcnQ6ZW52aXJvbm1lbnRzIjpbInNhbmRib3giXSwic3J0OmNsaWVudF9pZCI6IjQ0OTgzOSIsInNydDpjbGllbnRfaWRzIjpbIjQ0OTgzOSJdLCJzcnQ6em9uZV9jb2RlcyI6WyJhbnkiXSwic3J0OmZsZWV0X2lkcyI6WyIxIl0sInNydDpxdWVyaWVzIjpbIl9fc2NoZW1hIiwiX190eXBlbmFtZSIsIndob2FtaSIsInBhY2thZ2UiLCJwYWNrYWdlcyIsInpvbmVzIl0sInNydDptdXRhdGlvbnMiOlsicGFja2FnZSJdfQ.ywxA0s1alyYTKmpgCKNIlce9kiDbUBIunedhBdKOiDR3kTVEaJkJGRfKt3iO5qUpuPv08mfkgIBIRkVqHvmw1A',
    'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = response.json()
    stuart_response = json_response
    pricing_details = stuart_response.get('pricing',{})
    final_price = pricing_details.get("price_tax_included", {})
    delivery_pickup = stuart_response.get('pickup_at',{})
    delivery_details = stuart_response.get('deliveries',{})
    delivery_id = delivery_details.get("id", {})
    delivery_status = delivery_details.get("status", {})
    delivery_tracking = delivery_details.get("tracking_url", {})
    print(final_price)
    order.stuart_delivery_fee = final_price
    order.stuart_delivery_id = delivery_id
    order.stuart_tracking_url = delivery_tracking
    order.stuart_delivery_status = delivery_status
    order.stuart_collection = delivery_pickup
    order.save()
    return json_response

