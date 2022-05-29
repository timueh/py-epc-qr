"""Implements the command line interface (CLI)."""

import typer

app = typer.Typer()

from py_epc_qr import __version__
from py_epc_qr.checks import (
    check_amount,
    check_beneficiary,
    check_iban,
    check_remittance_unstructured,
    validate_prompt,
)
from py_epc_qr.transaction import consumer_epc_qr
from PIL import Image


@app.command()
def create(
    out: str = typer.Option(
        default="qr.png",
        help="name of generated qr png file",
    ),
    from_yaml: str = typer.Option(
        default="",
        help="specify yaml file from which to create qr",
    ),
):
    """
    Create EPC-compliant QR code for IBAN-based wire transfer within European economic area.
    """

    if from_yaml:
        typer.echo("creating qr code from yaml...")
        epc = consumer_epc_qr.from_yaml(from_yaml)
    else:
        beneficiary = typer.prompt("Enter the beneficiary", type=str)
        if not validate_prompt(check_beneficiary(beneficiary)):
            typer.echo("The beneficiary is not valid.")
            raise typer.Exit(code=1)
        iban = typer.prompt("Enter the IBAN", type=str)
        if not validate_prompt(check_iban(iban)):
            typer.echo("The IBAN appears incorrect.")
            raise typer.Exit(code=1)
        amount = typer.prompt("Enter the amount", type=float)
        if not validate_prompt(check_amount(amount)):
            typer.echo("The amount appears incorrect (must be float).")
            raise typer.Exit(code=1)
        remittance = typer.prompt("Enter reason for payment", type=str)
        if not validate_prompt(check_remittance_unstructured(remittance)):
            typer.echo("The value for the remittance appears incorrect.")
            raise typer.Exit(code=1)
        epc = consumer_epc_qr(beneficiary, iban, amount, remittance)

    epc.to_qr(out)
    typer.echo(f"🎉🎉🎉 You may view your png {out} 🎉🎉🎉")


@app.command()
def version():
    """
    Show version and exit.
    """
    typer.echo(f"py-epc-qr v{__version__}")
    raise typer.Exit()


@app.callback()
def main():
    """
    Create EPC-compliant QR codes for wire transfers.
    """
