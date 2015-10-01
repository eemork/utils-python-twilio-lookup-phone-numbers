# Download the Python helper library from twilio.com/docs/python/install
import csv
import sys
from twilio.rest import TwilioRestClient
from twilio.rest.lookups import TwilioLookupsClient
from config import ACCT, AUTH

num_dict = {"country_code": "",
            "phone_number": "",
            "national_format": "",
            "url": "",
            "carrier": {
                "mobile_country_code": "",
                "mobile_network_code": "",
                "name": "",
                "type": "",
                "error_code": ""}
            }

def lookup_phone_numbers(phone_numbers_file_name):

    skip_header = True
    total_pn_purchased = 0
    # Create a Twilio client connection
    client = TwilioLookupsClient(ACCT, AUTH)

    # Output results of lookup to a file
    results_file = phone_numbers_file_name + '_results.csv'
    fw = open(results_file, 'w')
    file_header = ["country_code", "phone_number", "carrier","mcc","mnc"]

    w = csv.DictWriter(fw, fieldnames=file_header, delimiter=',')
    w.writerow(dict((fn, fn) for fn in file_header))
    # Lookup phone numbers
    # Iterate through each phone number and do lookup
    dictReader = csv.DictReader(open(phone_numbers_file_name, 'rU'),
                                fieldnames=['phone_number'], delimiter=',', quotechar='"')
    for row in dictReader:
        if skip_header:
            # print 'File Header: ' + str(row)
            skip_header = False
            continue
        # Process content of csv file
        try:
            print("Looking Up: " + row['phone_number'])
            number = client.phone_numbers.get(row['phone_number'], include_carrier_info=True, country_code="US")
            num_dictionary = {}
            num_dictionary["country_code"] = number.country_code
            num_dictionary["phone_number"] = number.national_format
            num_dictionary["carrier"] = number.carrier['name']
            num_dictionary["mcc"] = number.carrier["mobile_country_code"]
            num_dictionary["mnc"] = number.carrier["mobile_network_code"]

            # print(number.phone_number)
            # print(number.carrier['name'])
            w.writerow(num_dictionary)
        except:
            print("bad number: " + row['phone_number'])
    fw.close()


# Main entry point
if __name__ == "__main__":
    account_sid = ACCT
    auth_token = AUTH
    if len(sys.argv) == 1:
        phone_numbers_file_name = 'phone_numbers.csv'
    else:
        phone_numbers_file_name = sys.argv[1]

    # Call the function
    print("Reading Input: " + phone_numbers_file_name)
    lookup_phone_numbers(phone_numbers_file_name)