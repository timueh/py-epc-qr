import typer

app = typer.Typer()

from py_epc_qr.transaction import consumer_epc_qr
from py_epc_qr.checks import check_beneficiary

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
        beneficiary = typer.prompt("Enter the beneficiary",value_proc=check_beneficiary)
        iban = typer.prompt("Enter the IBAN", type=str)
        amount = typer.prompt("Enter the amount", type=float)
        remittance = typer.prompt("Enter reason for payment", type=str)
        epc = consumer_epc_qr(beneficiary, iban, amount, remittance)
        epc.to_qr()
        typer.echo("Tadaaaa!")


@app.command()
def delete(
    username: str,
    force: bool = typer.Option(..., prompt="Are you sure you want to delete the user?"),
):
    if force:
        typer.echo(f"Deleting user: {username}")
    else:
        typer.echo("Operation cancelled")

if __name__ == "__main__":
    app()
