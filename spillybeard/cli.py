import click
import os

import spillybeard.beard as _beard


@click.group()
@click.pass_context
def entry_point(context):
    """\b
           __
        .-'  |        _____       _ ____      ____                      __
       /   <\|       / ___/____  (_) / /_  __/ __ )___  ____ __________/ /
      /     \\'       \__ \/ __ \/ / / / / / / __  / _ \/ __ `/ ___/ __  /
      |_.- o-o      ___/ / /_/ / / / / /_/ / /_/ /  __/ /_/ / /  / /_/ /
      / C  -._)\   /____/ .___/_/_/_/\__, /_____/\___/\__,_/_/   \__,_/
     /',  >o<   |      /_/          /____/
    |   `-,_,__,'                                             Nice beard.

    """
    context.obj = {}


@entry_point.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(exists=True),
    default=None,
    help="A place to keep bearded pics of your friendos.",
)
def embearden(filepath, output, before_and_after):
    """ Slap a SpillyBeard on that mug. """
    bearded_image = _beard.embearden(filepath)

    if output is None:
        bearded_image.show()
        return

    output_path = _beard.output_path(output, filepath)
    bearded_image.save(output_path)


@entry_point.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(exists=True),
    default=None,
    help="A place to keep bearded pics of your friendos.",
)
@click.option(
    "--vertical/--horizontal",
    default=True,
    help="You want ontop-guy, or a side-dealio?",
)
def before_and_after(filepath, output, vertical):
    """ Show your pals their Spilly potential. """
    bearded_image = _beard.make_before_and_after(filepath, vertical)
    if output is None:
        bearded_image.show()
        return

    output_path = _beard.output_path(output, filepath)
    bearded_image.save(output_path)
    return
