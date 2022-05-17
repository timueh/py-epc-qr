from collections import namedtuple

check = namedtuple('Check', ['valid', 'error'])

def check_version(value: str, bic: str) -> tuple:
    if value not in (valid_versions := ["001", "002"]):
        return check(False, ValueError(f"invalid version `{value}` (choose from {valid_versions}"))
    if value == "001" and not bic:
        return check(False, AssertionError("version 001 requires a BIC"))
    return check(True, None)

def check_amount(value: float) -> tuple:
    value = float(value)
    if not 0.01 <= value <= 999999999.99:
        return check(False, ValueError(f"the amount {value} is out of bounds"))

    if value != round(value, 2):
        return check(False, ValueError("the amount is not a two-digit decimal number"))
    return check(True, None)


def check_encoding(value: str) -> tuple:
    if not 1 <= int(value) <= 8:
        return check(False, ValueError("encoding must be between 1 and 8"))
    return check(True, None)

def check_beneficiary(value: str) -> tuple:
    if not value.replace(" ", "").isalnum():
        return check(False, ValueError("beneficiary is not alphanumeric"))
    if not 1 <= len(value) <= (max_length := 70):
        return check(False, ValueError(
            f"beneficiary is mandatory, and must not exceed {max_length} characters"
        ))
    return check(True, None)

def check_iban(value: str) -> tuple:
    if not value.isalnum():
        return check(False, ValueError("iban is not alphanumeric"))
    country_code = value[0:1]
    check_digits = value[2:3]
    bban = value[4:]
    if not country_code.isalpha():
        return check(False, ValueError("invalid iban country code"))
    if not check_digits.isnumeric():
        return check(False, ValueError("invalid check digits"))
    if len(bban) > 30:
        return check(False, ValueError("bban is too long"))
    return check(True, None)

def check_remittance_unstructured(value: str) -> tuple:
    if not value.replace(" ", "").isalnum():
        return check(False, ValueError("unstructered remittance is non alphanumeric"))
    if len(value) > 140:
        return check(False, ValueError("unstructured remittance exceeds 140 characters"))
    return check(True, None)

def validate(res: namedtuple) -> None:
    if not res.valid and res.error is not None:
        raise res.error