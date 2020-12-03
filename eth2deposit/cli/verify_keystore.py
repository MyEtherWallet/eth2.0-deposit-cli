import click
from eth2deposit.key_handling.keystore import (
    Keystore,
)
import json
from py_ecc.bls import G2ProofOfPossession as bls


@click.command(
    help='verify existing generated keystore',
)
@click.pass_context
@click.option(
    '--keystore_path',
    help=('path to the keystore file'),
    prompt='Please enter the path to keystore file',
    required=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.password_option(
    '--keystore_password',
    help=('The password that you used to secure your keystores.'),
    prompt='Type the password that secures your validator keystore(s)',
    required=True,
    type=str,
)
def verify_keystore(ctx: click.Context, keystore_path: str, keystore_password: str) -> bool:
    with open(keystore_path, 'r') as f:
        fjson = json.load(f)
    saved_keystore = Keystore.from_json(fjson)
    try:
        secret_bytes = saved_keystore.decrypt(keystore_password)
    except ValueError:
        print("Invalid password!")
    else:
        if (bls.SkToPk(int.from_bytes(secret_bytes, 'big')).hex() == fjson['pubkey']):
            click.echo('\nSuccess!\nYour keystore is valid')
        else:
            click.echo('\nError!\nYour keystore is invalid')
