import filecmp
from os import remove

import PIL
import pytest
import qrcode

from py_epc_qr import __version__
from py_epc_qr.transaction import consumer_epc_qr, epc_qr


def test_version():
    assert __version__ == "0.1.0"


def get_valid_dummy_iban():
    return "DE" + "1" * 18


class TestEpcQr:
    @pytest.mark.parametrize(
        "fun, given, expected_txt, expected_png",
        [
            (
                consumer_epc_qr,
                {
                    "beneficiary": "Wikimedia Foerdergesellschaft",
                    "iban": "DE33100205000001194700",
                    "amount": 123.45,
                    "remittance": "Spende fuer Wikipedia",
                },
                "tests/data/qr_version_002.txt",
                "tests/data/qr_version_002.png",
            ),
            (
                epc_qr,
                {
                    "version": "001",
                    "encoding": 1,
                    "bic": "BFSWDE33BER",
                    "beneficiary": "Wikimedia Foerdergesellschaft",
                    "iban": "DE33100205000001194700",
                    "amount": 123.45,
                    "purpose": "",
                    "remittance_structured": "",
                    "remittance_unstructured": "Spende fuer Wikipedia",
                    "originator_information": "",
                },
                "tests/data/qr_version_001.txt",
                "tests/data/qr_version_001.png",
            ),
        ],
    )
    def test_epc_qr_version(self, fun, given, expected_txt, expected_png):
        """
        Given the QR example from wikipedia
        When creating an epc_qr as txt and png
        Then everything works as intended
        """
        qr = fun(**given)
        qr.to_txt(tmp_txt := "out.txt")
        qr.to_qr(tmp_png := "out.png")
        assert filecmp.cmp(tmp_txt, expected_txt)
        assert filecmp.cmp(tmp_png, expected_png)
        remove(tmp_txt)
        remove(tmp_png)

    @pytest.mark.parametrize("value", [0, 9])
    def test_epc_qr_encoding_raises_exception(self, value):
        with pytest.raises(ValueError):
            epc_qr(
                version="002",
                encoding=value,
                bic="",
                beneficiary="ben benefit",
                iban=get_valid_dummy_iban(),
                amount=10,
                purpose="",
                remittance_structured="",
                remittance_unstructured="",
                originator_information="",
            )

    @pytest.mark.parametrize(
        "value",
        [
            0,
            -1,
            999999999.99 + 0.01,
            10.001,
            0.011,
            "0",
            "-1",
            "999999999.99+0.01",
            "10.001",
            "0.011",
            "abc",
        ],
    )
    def test_epc_qr_amount_raises_exception(self, value):
        """
        Given an invalid amount
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(ValueError):
            consumer_epc_qr("me", get_valid_dummy_iban(), value, "")

    @pytest.mark.parametrize("value", ["", "a" * 71, "§23"])
    def test_epc_qr_beneficiary_raises_exception(self, value):
        """
        Given an beneficiary that is too long
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(ValueError):
            consumer_epc_qr(value, get_valid_dummy_iban(), 12.20, "something")

    @pytest.mark.parametrize("value", ["000", "00", "0", "003"])
    def test_epc_qr_version_raises_exception(self, value):
        """
        Given an beneficiary that is too long
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(ValueError):
            epc_qr(value, 1, "", "", get_valid_dummy_iban(), "", "", "", "", "")

    def test_epc_qr_version_001_with_empty_bic_raises_exception(self):
        """
        Given version 001 and an empty bic
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(AssertionError):
            epc_qr("001", 1, "", "", get_valid_dummy_iban(), 10.00, "", "", "", "")

    @pytest.mark.parametrize(
        "value", ["123", "DEA1", "DE12%", "DE12" + "a" * 31, "Hallo ,:"]
    )
    def test_epc_qr_iban_invalid_raises_exception(self, value):
        """
        Given an iban with an invalid country code
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(ValueError):
            consumer_epc_qr("ben benefit", value, 0.01, "")

    @pytest.mark.parametrize("value", ["DE12%", "a" * 141, "%" * 141])
    def test_epc_qr_unstructured_remittance_raises_exception(self, value):
        """
        Given an iban with an invalid country code
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(ValueError):
            consumer_epc_qr("ben benefit", get_valid_dummy_iban(), 0.01, value)

    def test_epc_qr_from_yaml(self):
        epc_qr_src = consumer_epc_qr.from_yaml("tests/template_version_002.yaml")
        epc_qe_tgt = consumer_epc_qr(
            beneficiary="Wikimedia Foerdergesellschaft",
            iban="DE33100205000001194700",
            amount=10,
            remittance="Danke",
        )
        assert epc_qr_src.to_txt() == epc_qe_tgt.to_txt()

    def test_epc_qr_from_yaml_raises_exception(self):
        with pytest.raises(AssertionError):
            consumer_epc_qr.from_yaml("tests/template_version_002_broken.yaml")
