import qrcode
import yaml

from py_epc_qr.constants import ALLOWED_KEYS, ROW_MAPPING, ENCODINGS
from py_epc_qr.checks import check_beneficiary, check_version, check_amount, check_encoding, check_iban, check_remittance_unstructured, validate


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
        originator_information: str,
    ):
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

    def to_txt(self, file_name: str = "qr_source.txt"):
        with open(file_name, "w", encoding=self.resolve_encoding()) as file:
            for key, value in ROW_MAPPING.items():
                file.write(self.__getattribute__(value))
                if key < 12:
                    file.write("\n")

    def to_str(self) -> str:
        res = ""
        for key, value in ROW_MAPPING.items():
            res += self.__getattribute__(value)
            if key < 12:
                res += "\n"
        return res

    def to_qr(self, file_name: str = "qr.png"):
        qr = qrcode.QRCode(
            version=6,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
        )
        qr.add_data(self.to_str())
        qr.make()
        img = qr.make_image()
        img.save(file_name)
        print("created image")

    # Properties

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value: str):
        validate(check_version(value, self.bic))
        self.__version = value

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        validate(check_amount(value))
        self.__amount = "EUR{:.2f}".format(float(value))

    @property
    def encoding(self):
        return self.__encoding

    @encoding.setter
    def encoding(self, value):
        validate(check_encoding(value))

        self.__encoding = str(value)

    def resolve_encoding(self) -> str:
        return ENCODINGS[int(self.encoding)]

    @property
    def beneficiary(self):
        return self.__beneficiary

    @beneficiary.setter
    def beneficiary(self, value: str):
        validate(check_beneficiary(value))
        self.__beneficiary = value


    @property
    def iban(self):
        return self.__iban

    @iban.setter
    def iban(self, value: str):
        validate(check_iban(value))
        self.__iban = value

    @property
    def remittance_unstructured(self):
        return self.__remittance_unstructured

    @remittance_unstructured.setter
    def remittance_unstructured(self, value):
        validate(check_remittance_unstructured(value))
        self.__remittance_unstructured = value


class consumer_epc_qr(epc_qr):
    def __init__(self, beneficiary: str, iban: str, amount: float, remittance: str):
        super().__init__(
            version="002",
            encoding=1,
            bic="",
            beneficiary=beneficiary,
            iban=iban,
            amount=amount,
            purpose="",
            remittance_structured="",
            remittance_unstructured=remittance,
            originator_information="",
        )

    @classmethod
    def from_yaml(cls, file_name: str):
        with open(file_name, "r") as file:
            data = yaml.safe_load(file)
        if not sorted(list(data.keys())) == sorted(ALLOWED_KEYS):
            raise AssertionError(
                f"yaml template has incorrect entries (allowed are {ALLOWED_KEYS})"
            )
        return cls(**data)


if __name__ == "__main__":
    epc = consumer_epc_qr.from_yaml("template.yaml")
    epc = consumer_epc_qr(
        "Wikimedia Fördergesellschaft", "DE33100205000001194700", 1, "Danke"
    )
    epc.to_qr()
