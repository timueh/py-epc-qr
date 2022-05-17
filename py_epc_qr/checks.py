
def check_version(value: str, bic: str) -> tuple:
    if value not in (valid_versions := ["001", "002"]):
        return False, ValueError(f"invalid version `{value}` (choose from {valid_versions}")
    if value == "001" and not bic:
        return False, AssertionError("version 001 requires a BIC")
    return True, None

def check_amount(value: float) -> tuple:
    value = float(value)
    if not 0.01 <= value <= 999999999.99:
        return False, ValueError(f"the amount {value} is out of bounds")

    if value != round(value, 2):
        return False, ValueError("the amount is not a two-digit decimal number")
    return True, None


def check_encoding(value: str) -> tuple:
    if not 1 <= int(value) <= 8:
        return False, ValueError("encoding must be between 1 and 8")
    return True, None

def check_beneficiary(value: str) -> tuple:
    if not value.replace(" ", "").isalnum():
        return False, ValueError("beneficiary is not alphanumeric")
    if not 1 <= len(value) <= (max_length := 70):
        return False, ValueError(
            f"beneficiary is mandatory, and must not exceed {max_length} characters"
        )
    return True, None

def check_iban(value: str) -> tuple:
    if not value.isalnum():
        return False, ValueError("iban is not alphanumeric")
    country_code = value[0:1]
    check_digits = value[2:3]
    bban = value[4:]
    if not country_code.isalpha():
        return False, ValueError("invalid iban country code")
    if not check_digits.isnumeric():
        return False, ValueError("invalid check digits")
    if len(bban) > 30:
        return False, ValueError("bban is too long")
    return True, None

def check_remittance_unstructured(value: str) -> tuple:
    if not value.replace(" ", "").isalnum():
        return False, ValueError("unstructered remittance is non alphanumeric")
    if len(value) > 140:
        return False, ValueError("unstructured remittance exceeds 140 characters")
    return True, None