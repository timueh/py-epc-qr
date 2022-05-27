"""Core functionality that converts epc qr code format to qr code image."""

import qrcode
import yaml

from py_epc_qr.checks import (
    check_amount,
    check_beneficiary,
    check_encoding,
    check_iban,
    check_remittance_unstructured,
    check_version,
    validate,
)
from py_epc_qr.constants import ALLOWED_KEYS, ENCODINGS, ROW_MAPPING


class epc_qr:
    """
    Class containing epc qr code specification and its conversion to image/text.
    """
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
        """Initialize"""
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

    def to_txt(self, file_name: str = "qr_source.txt") -> None:
        """
        Write EPC-compliant string to text file `file_name`
        """
        with open(file_name, "w", encoding=self.resolve_encoding()) as file:
            for key, value in ROW_MAPPING.items():
                file.write(self.__getattribute__(value))
                if key < 12:
                    file.write("\n")

    def to_str(self) -> str:
        """
        Write EPC-compliant string.
        """
        res = ""
        for key, value in ROW_MAPPING.items():
            res += self.__getattribute__(value)
            if key < 12:
                res += "\n"
        return res

    def to_qr(self, file_name: str = "qr.png"):
        """
        Write EPC-compliant string to png image `file_name`
        """
        qr = qrcode.QRCode(
            version=6,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
        )
        qr.add_data(self.to_str())
        qr.make()
        img = qr.make_image()
        img.save(file_name)
        print("created image")

    # Properties of class

    @property
    def version(self) -> str:
        """
        Return EPC version entry.
        """
        return self.__version

    @version.setter
    def version(self, value: str):
        """
        Set EPC version entry.
        """
        validate(check_version(value, self.bic))
        self.__version = value

    @property
    def amount(self) -> str:
        """
        Return EPC amount entry.
        """
        return self.__amount

    @amount.setter
    def amount(self, value):
        """
        Set and validate EPC amount entry.
        """
        validate(check_amount(value))
        self.__amount = "EUR{:.2f}".format(float(value))

    @property
    def encoding(self) -> str:
        """
        Return EPC encoding entry.
        """
        return self.__encoding

    @encoding.setter
    def encoding(self, value) -> None:
        """
        Set and validate EPC encoding entry.
        """
        validate(check_encoding(value))
        self.__encoding = str(value)

    def resolve_encoding(self) -> str:
        """
        Resolve EPC encoding entry.
        """
        return ENCODINGS[int(self.encoding)]

    @property
    def beneficiary(self) -> str:
        """
        Return EPC beneficiary entry.
        """
        return self.__beneficiary

    @beneficiary.setter
    def beneficiary(self, value: str) -> None:
        """
        Set and validate EPC beneficiary entry.
        """
        validate(check_beneficiary(value))
        self.__beneficiary = value

    @property
    def iban(self) -> str:
        """
        Return EPC iban entry.
        """
        return self.__iban

    @iban.setter
    def iban(self, value: str):
        """
        Set and validate EPC iban entry.
        """
        validate(check_iban(value))
        self.__iban = value

    @property
    def remittance_unstructured(self) -> str:
        """
        Return EPC unstructured remittance entry.
        """
        return self.__remittance_unstructured

    @remittance_unstructured.setter
    def remittance_unstructured(self, value) -> None:
        """
        Set and validate EPC unstructured remittance entry.
        """
        validate(check_remittance_unstructured(value))
        self.__remittance_unstructured = value


class consumer_epc_qr(epc_qr):
    """
    Standard consumer EPC QR code for IBAN-based wire transfer within European economic area.
    """
    def __init__(self, beneficiary: str, iban: str, amount: float, remittance: str):
        """Initialize"""
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
        """Create from yaml file"""
        with open(file_name, "r") as file:
            data = yaml.safe_load(file)
        if not sorted(list(data.keys())) == sorted(ALLOWED_KEYS):
            raise AssertionError(
                f"yaml template has incorrect entries (allowed are {ALLOWED_KEYS})"
            )
        return cls(**data)
