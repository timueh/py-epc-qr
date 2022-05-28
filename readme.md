# Create QR codes for wire transfers

Sick of copy-and-pasting IBANs to forms?
Why not just scan a QR code and have your favorite banking app take care of the rest?

Why not be generous and support wikipedia with 123,45€?
Grab your phone and scan the image.

![Support Wikipedia with 123,45 €](tests/data/qr_version_002.png "Support Wikipedia with 123,45 €")

[The create QR code complies with the European Payments Council (EPC) Quick Response (QR) code guidelines.](https://en.wikipedia.org/wiki/EPC_QR_code)

Disclaimer: The author of this code has no affiliation with the EPC whatsoever.
Henceforth, you are welcome to use the code at your own dispense, but any use is at your own (commercial) risk.

## Installation

You can easily install the Python package via pip.

```python
pip install py-epc-qr
```

## Usage

You can use the package as part of your own code or as a standalone command line interface (CLI).

### Code

```python
from py_epc_qr.transaction import consumer_epc_qr
epc_qr = consumer_epc_qr(
    beneficiary= "Wikimedia Foerdergesellschaft",
    iban= "DE33100205000001194700",
    amount= 123.45,
    remittance= "Spende fuer Wikipedia"
    )
epc_qr.to_qr()
```

### CLI

<todo>

### From interaction

<todo>

#### From template

<todo>

## Limitations

Currently, the EPC specifications are implemented only to work with IBAN-based consumer wire transfers within the European Economic Area.