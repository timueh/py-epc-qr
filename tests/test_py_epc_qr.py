from py_epc_qr import __version__
from py_epc_qr.transaction import consumer_epc_qr, epc_qr

import pytest


def test_version():
    assert __version__ == '0.1.0'

def get_valid_dummy_iban():
    return 'DE' + '1'*18

class TestEpcQr:

    @pytest.mark.parametrize('value', [
        0,
        -1,
        999999999.99+0.01,
        10.001,
        0.011,
        '0',
        '-1',
        '999999999.99+0.01',
        '10.001',
        '0.011',
    ])
    def test_epc_qr_amount_raises_exception(self, value):
        """
        Given an invalid amount
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(ValueError):
            consumer_epc_qr('me', get_valid_dummy_iban(), value, '')

    @pytest.mark.parametrize('value', ['a'*71, '§23'])
    def test_epc_qr_beneficiary_raises_exception(self, value):
        """
        Given an beneficiary that is too long
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(ValueError):
            consumer_epc_qr(value, get_valid_dummy_iban(), 12.20, 'something')

    @pytest.mark.parametrize('value', ['000', '00', '0', '003'])
    def test_epc_qr_version_raises_exception(self, value):
        """
        Given an beneficiary that is too long
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(ValueError):
            epc_qr(value,1,'','',get_valid_dummy_iban(),'','','','','')
        
    def test_epc_qr_version_001_with_empty_bic_raises_exception(self):
        """
        Given version 001 and an empty bic
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(AssertionError):
            epc_qr('001', 1, '', '', get_valid_dummy_iban(), 10.00, '', '', '', '')

    @pytest.mark.parametrize('value', ['123', 'DEA1', 'DE12%', 'DE12' + 'a' * 31])
    def test_epc_qr_iban_invalid_raises_exception(self, value):
        """
        Given an iban with an invalid country code
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(ValueError):
            consumer_epc_qr('',value,0.01,'')

    @pytest.mark.parametrize('value', ['DE12%', 'a' * 141, '%' * 141])
    def test_epc_qr_unstructured_remittance_raises_exception(self, value):
        """
        Given an iban with an invalid country code
        When creating an epc qr
        Then an exception is raised
        """
        with pytest.raises(ValueError):
            consumer_epc_qr('',get_valid_dummy_iban(),0.01,value)