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
@click.option(
    "--style",
    "-s",
    type=click.Choice(["real", "mask", "nomouth", "mouth", "derp"]),
    default="real",
    help="Which beard style you want.",
)
def embearden(filepath, output, style):
    """ Slap a SpillyBeard on that mug. """
    bearded_image = _beard.embearden(filepath, style=style)
    if bearded_image is None:
        click.echo("Could not process this image!")
        return

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
    "--style",
    "-s",
    type=click.Choice(["real", "mask", "nomouth", "mouth", "derp"]),
    default="real",
    help="Which beard style you want.",
)
@click.option(
    "--vertical/--horizontal",
    default=True,
    help="You want ontop-guy, or a side-dealio?",
)
def before_and_after(filepath, output, style, vertical):
    """ Show your pals their Spilly potential. """
    bearded_image = _beard.make_before_and_after(filepath, style, vertical)

    if bearded_image is None:
        click.echo("Could not process this image!")
        return

    if output is None:
        bearded_image.show()
        return

    output_path = _beard.output_path(output, filepath)
    bearded_image.save(output_path)
    return
