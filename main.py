import typer
import sys

# sys.path.insert(0, 'python_argparse')
# print(sys.path)
# from python_argparse.main import main

app = typer.Typer()
subapp = typer.Typer(name='sub')
app.add_typer(subapp)

@app.callback(invoke_without_command=True)
def callback(what:str='callback_what'):
    print(f'callback {what = }')

@subapp.callback(invoke_without_command=True)
def subcallback(what:str='subcallback_what'):
    print(f'subcallback {what = }')

@app.command()
def main(name:str, capitalize:bool=False):
    print(f'main {name = }, {capitalize = }')

@subapp.command('main')
def submain(name:str):
    print(f'sub {name = }')

# typer.run(
    # main
# )
app()
