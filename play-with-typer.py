import typer

import sys
# sys.path.insert(0, 'python_argparse')
# print(sys.path)
# from python_argparse.main import main

app = typer.Typer()
subapp = typer.Typer(name='sub')
app.add_typer(subapp)


@app.callback(invoke_without_command=True)
def callback(ctx:typer.Context, what:str='callback_what'):
    print(f'callback {what = }')
    ctx.ensure_object(dict)
    ctx.obj['what'] = what
    print(f'callback {ctx.obj = }')


@subapp.callback(invoke_without_command=True)
def subcallback(ctx:typer.Context, what:str='subcallback_what'):
    print(f'subcallback {what = }')
    ctx.obj['subwhat'] = what
    print(f'subcallback {ctx.obj = }')


@app.command()
def main(ctx:typer.Context, name:str, capitalize:bool=False):
    print(f'main {name = }, {capitalize = }')
    ctx.obj['main'] = {
        'name': name,
        'capitalize': capitalize
    }
    print(f'main {ctx.obj = }')
    


@subapp.command('main')
def submain(ctx:typer.Context, name:str):
    print(f'sub {name = }')
    ctx.obj['submain'] = {
        'name': name,
    }
    print(f'main {ctx.obj = }')

# typer.run(
    # main
# )
app()
