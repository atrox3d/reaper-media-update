import typer
import logging

from proxy import (
    simplegit,
    filters,
    options,
    output,
    config
)

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.callback(invoke_without_command=True)
def init(ctx:typer.Context):
    logging.basicConfig(
        level=logging.DEBUG
    )
    
    cfg = config.JsonConfig().load()
    
    ctx.ensure_object(dict)
    ctx.obj['cfg'] = cfg


@app.command()
def main(ctx:typer.Context):
    print(f'{ctx.obj = }')


if __name__ == "__main__":
    app()