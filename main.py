from pathlib import Path

import click

import runners.utils


@click.group()
def cli():
    pass


@cli.command(name="simulator")
def run_simulator():
    from runners import simulator

    simulator.run()


@cli.command(name="kiosk")
@click.option(
    "-s",
    "--simulate",
    is_flag=True,
    default=False,
    help="Run in simulated environment.",
)
@click.option(
    "-t",
    "--test",
    is_flag=True,
    default=False,
    help="Run in test mode. This shortens the demo time and user input time "
    "for testing purposes.",
)
def run_kiosk(simulate, test):
    from runners import kiosk

    kiosk.run(simulate, testing=test)


@cli.command("demo")
@click.argument(
    "name",
    type=click.Choice(
        [name for name, _ in runners.utils.get_demos()], case_sensitive=False
    ),
)
@click.option(
    "-s",
    "--simulate",
    is_flag=True,
    default=False,
    help="Run in simulated environment.",
)
@click.option(
    "-t",
    "--test",
    is_flag=True,
    default=False,
    help="Run in test mode. This provides feedback for if your demo is "
    "running fast enough relative to the set frame rate.",
)
def run_demo(name, simulate, test):
    from runners import demo

    demo.run(name, simulate, testing=test)


if __name__ == "__main__":
    cli()
