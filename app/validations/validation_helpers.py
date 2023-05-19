"""
Methods that help with the validation process
"""
import pycountry


def get_country_name(country_code):
    country = pycountry.countries.get(alpha_2=country_code)
    return country.name if country else None


def extract_iban_details(iban):
    country_code = iban[:2]
    check_digits = iban[2:4]
    bank_code = iban[4:8]
    account_number = iban[8:]

    country_name = get_country_name(country_code)

    return {
        "country_code": country_code,
        "country_name": country_name,
        "check_digits": check_digits,
        "bank_code": bank_code,
        "account_number": account_number,
    }
