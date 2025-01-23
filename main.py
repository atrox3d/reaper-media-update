import typer
import sys

# sys.path.insert(0, 'python_argparse')
# print(sys.path)
# from python_argparse.main import main
app = typer.Typer()


@app.command()
def main(name:str):
    print('hello ' + name)


@app.command()
def mein(name:str):
    print('hello ' + name)


# typer.run(
    # main
# )
app()
