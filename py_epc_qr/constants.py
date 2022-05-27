"""Constants according to epc qr code specification."""

ALLOWED_KEYS = ["beneficiary", "iban", "amount", "remittance"]

ROW_MAPPING = {
    1: "bcd",
    2: "version",
    3: "encoding",
    4: "identification_code",
    5: "bic",
    6: "beneficiary",
    7: "iban",
    8: "amount",
    9: "purpose",
    10: "remittance_structured",
    11: "remittance_unstructured",
    12: "originator_information",
}

ENCODINGS = {
    1: "UTF-8",
    2: "ISO-8859-1",
    3: "ISO-8859-2",
    4: "ISO-8859-4",
    5: "ISO-8859-5",
    6: "ISO-8859-7",
    7: "ISO-8859-10",
    8: "ISO-8859-15",
}
