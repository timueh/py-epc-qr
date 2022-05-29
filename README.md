[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/timueh/py-epc-qr/branch/main/graph/badge.svg?token=LMQKVGWT2W)](https://codecov.io/gh/timueh/py-epc-qr)
![tests](https://github.com/timueh/py-epc-qr/actions/workflows/pytest.yml/badge.svg)
![lint_with_black](https://github.com/timueh/py-epc-qr/actions/workflows/black.yml/badge.svg)

# Create QR codes for wire transfers

Sick of copy-and-pasting IBANs to forms?
Why not just scan a QR code and have your favorite banking app take care of the rest?

Why not be generous and support wikipedia with EUR10?
Grab your phone and scan the image (created with this tool).

![Support Wikipedia with 10 €](tests/data/qr_wikimedia.png "Support Wikipedia with 10 €")

[The created QR code complies with the European Payments Council (EPC) Quick Response (QR) code guidelines.](https://en.wikipedia.org/wiki/EPC_QR_code)

**1st Disclaimer**: The author of this code has no affiliation with the EPC whatsoever.
Henceforth, you are welcome to use the code at your own dispense, but any use is at your own (commercial) risk.

**2nd Disclaimer**: Currently, the EPC specifications are implemented only to work with IBAN-based consumer wire transfers within the European Economic Area (EEA), i.e. using the following pieces of information:

- Recipient
- IBAN
- Amount
- Unstructured remittance (aka reason for transfer)

Of course, any helping hand is welcome to extend the core functionality to more generic transactions.

## Installation

To use the code as a standalone command line interface (CLI) tool, then use [`pipx`](https://pypa.github.io/pipx/) as follows

```bash
pipx install py-epc-qr
```

You may verify the installation by calling `epcqr version`.
The output should be identical to what `pipx` printed.

If you intend to use the code instead directly in your own Python projects, then install the package using `pip`

```bash
pip install py-epc-qr
```


## Usage

You may use the package as a standalone command line interface (CLI) or as part of your own code.

### CLI

Having installed the package with `pipx` (see [above](#installation)), you may verify the installation upon calling

```bash
>> epcqr --help
Usage: epcqr [OPTIONS] COMMAND [ARGS]...

  Create EPC-compliant QR codes for wire transfers.

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  create   Create EPC-compliant QR code for IBAN-based wire transfer...
  version  Show version and exit.
```

The last lines show the available commands.

The core functionality lies behind `create`, for which you can call again the `help`.

```bash
epcqr create --help     
Usage: epcqr create [OPTIONS]

  Create EPC-compliant QR code for IBAN-based wire transfer within European
  economic area.

Options:
  --out TEXT        name of generated qr png file  [default: qr.png]
  --from-yaml TEXT  specify yaml file from which to create qr
  --help            Show this message and exit.
```

#### From interaction

If you call the `create` command without any options, it is started in an interactive mode.
You are asked to input all relevant information.
If your input is correct, an image will be created in your current directory.

#### From template

Alternatively, you can create the QR code from a `yaml` template, [for which the repository contains an example](template.yaml).

### Code

If you intend to use the source code in your own Python projects, then a minimal working example looks as follows:

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

The relevant functions are gathered in [`transaction.py`](py_epc_qr/transaction.py)

