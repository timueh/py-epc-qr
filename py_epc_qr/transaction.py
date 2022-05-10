import qrcode

rows = {
    1: 'bcd',
    2: 'version',
    3: 'encoding',
    4: 'identification_code',
    5: 'bic',
    6: 'beneficiary',
    7: 'iban',
    8: 'amount',
    9: 'purpose',
    10: 'remittance_structured',
    11: 'remittance_unstructured',
    12: 'originator_information'
}

ENCODINGS = {
    1: 'UTF-8',
    2: 'ISO-8859-1',
    3: 'ISO-8859-2',
    4: 'ISO-8859-4',
    5: 'ISO-8859-5',
    6: 'ISO-8859-7',
    7: 'ISO-8859-10',
    8: 'ISO-8859-15',
}

class epc_qr:
    def __init__(
                self,
                version: str,
                encoding: int,
                bic: str,
                beneficiary: str,
                iban: str,
                amount: float,
                purpose: str,
                remittance_structured: str,
                remittance_unstructured: str,
                originator_information: str):
        self.bcd = "BCD"
        self.bic = bic
        self.version = version
        self.encoding = encoding
        self.identification_code = "SCT"
        self.beneficiary = beneficiary
        self.iban = iban
        self.amount = amount
        self.purpose = purpose
        self.remittance_structured = remittance_structured
        self.remittance_unstructured = remittance_unstructured
        self.originator_information = originator_information

    def to_txt(self, file_name: str = 'qr_source.txt'):
        with open(file_name, 'w', encoding=self.resolve_encoding()) as file:
            for key, value in rows.items():
                file.write(self.__getattribute__(value))
                if key < 12:
                    file.write('\n')

    def to_str(self) -> str:
        res = ''
        for key, value in rows.items():
            res += self.__getattribute__(value)
            if key < 12:
                res += '\n'
        return res

    def to_qr(self, file_name: str = 'qr.png'):
        qr = qrcode.QRCode(
            version=6,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
        )
        qr.add_data(self.to_str())
        qr.make()
        img = qr.make_image()
        img.save(file_name)
        print(f'created image')

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value: str):
        if value not in (valid_versions:=['001', '002']):
            raise ValueError(f'invalid version `{value}` (choose from {valid_versions}')
        if value == '001' and not self.bic:
            raise AssertionError('version 001 requires a BIC')
        self.__version = value

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        value = float(value)
        if not 0.01 <= value <= 999999999.99:
            raise ValueError(f'the amount {value} is out of bounds')

        if value != round(value, 2):
            raise ValueError(f'the amount is not a two-digit decimal number')
        self.__amount = 'EUR{:.2f}'.format(value)

    @property
    def encoding(self):
        return self.__encoding

    @encoding.setter
    def encoding(self, value):
        if not 1 <= int(value) <= 8:
            raise ValueError('encoding must be between 1 and 8')

        self.__encoding = str(value)

    def resolve_encoding(self) -> str:
        return ENCODINGS[int(self.encoding)]

    @property
    def beneficiary(self):
        return self.__beneficiary

    @beneficiary.setter
    def beneficiary(self, value: str):
        if not value.replace(" ", "").isalnum():
            raise ValueError('beneficiary is not alphanumeric')
        if len(value) > (max_length:=70):
            raise ValueError(f'beneficiary must nood exceed {max_length} characters')
        self.__beneficiary = value

    @property
    def iban(self):
        return self.__iban
    
    @iban.setter
    def iban(self, value):
        if not value.isalnum():
            raise ValueError('iban is not alphanumeric')
        country_code = value[0:1]
        check_digits = value[2:3]
        bban = value[4:]
        if not country_code.isalpha():
            raise ValueError('invalid iban country code')
        if not check_digits.isnumeric():
            raise ValueError('invalid check digits')
        if len(bban) > 30:
            raise ValueError('bban is too long')
        self.__iban = value

    @property
    def remittance_unstructured(self):
        return self.__remittance_unstructured

    @remittance_unstructured.setter
    def remittance_unstructured(self, value):
        if not value.replace(" ", "").isalnum():
            raise ValueError('unstructered remittance is non alphanumeric')
        if len(value) > 140:
            raise ValueError('unstructured remittance exceeds 140 characters')
        self.__remittance_unstructured = value


class consumer_epc_qr(epc_qr):
    def __init__(self, beneficiary: str,
                 iban: str,
                 amount: float,
                 remittance: str):
        super().__init__(
            version='002',
            encoding=1,
            bic='',
            beneficiary=beneficiary,
            iban=iban,
            amount=amount,
            purpose='',
            remittance_structured='',
            remittance_unstructured=remittance,
            originator_information='',
        )


if __name__ == "__main__":
    epc = consumer_epc_qr('rolf beneficiary', 'DE18200411550436942700', 12.34, 'my reference')
    epc.to_txt()
    epc.to_qr()
    breakpoint()