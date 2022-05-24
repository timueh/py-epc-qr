import typer

app = typer.Typer()

from py_epc_qr.transaction import consumer_epc_qr
from py_epc_qr.checks import check_beneficiary, check_iban, check_amount, validate_prompt, check_remittance_unstructured

@app.command()
def create(
    out: str = typer.Option(
        default="qr.png",
        help="name of generated qr png file",
    ),
    from_yaml: str = typer.Option(
        default="",
        help="specify yaml file from which to create qr",
    )):

    if from_yaml:
        typer.echo(f"creating from yaml...")
        epc = consumer_epc_qr.from_yaml(from_yaml)
        epc.to_qr(out)
        typer.echo(f"success: you may view your png {out}")
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
        typer.echo("Tadaaaa!")

def version_callback(value: bool):
    if value:
        typer.echo(f"Awesome CLI Version: {__version__}")
        raise typer.Exit()

@app.callback()
def callback():
    pass

if __name__ == "__main__":
    app()
