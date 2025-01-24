import typer
import logging
from enum import Enum

from proxy import (
    simplegit,
    filters,
    options,
    output,
    config
)


logger = logging.getLogger(__name__)
app = typer.Typer()


choices = list(
    zip(
        list(logging.getLevelNamesMapping()),
        list(logging.getLevelNamesMapping()),
    )
)
LogLevels = Enum('LogLevels', choices)


@app.callback(invoke_without_command=True)
def init(ctx:typer.Context, log_level:LogLevels = 'INFO'):
    logging.basicConfig(
        level=log_level.value
    )
    
    cfg = config.JsonConfig().load()
    
    ctx.ensure_object(dict)
    ctx.obj['cfg'] = cfg
    ctx.obj['log_level'] = log_level


@app.command()
def main(ctx:typer.Context):
    logger.info(f'{ctx.obj = }')
    
    # test --log-level
    logger.debug('test')
    logger.info('test')
    logger.warning('test')
    logger.error('test')
    logger.fatal('test')


if __name__ == "__main__":
    app()