from typing import Optional

import click
import rumps

from asana_api import AsanaClient
from macos import macos_app, get_task_name_updater


@click.group()
def cli():
    """
    asana_macos_statusbar displays your current task in MacOS statusbar.
    """


@cli.command()
@click.argument('access_token')
@click.option('--section-id', default=None)
@click.option('--tag-id', default=None)
@click.option('--project-id', default=None)
@click.option('--interval', default=60, show_default=True)
def run(access_token: str, section_id: Optional[str], tag_id: Optional[str], project_id: Optional[str], interval: int):
    """
    Run asana_macos_statusbar.

    Before launch you should make new access_token — https://asana.com/guide/help/api/api

    Choose one of the ways: retrieving tasks from section, tag or project and set id with corresponding CLI option.
    """
    client = AsanaClient(
        access_token,
        section_id=section_id,
        tag_id=tag_id,
        project_id=project_id,
    )
    rumps.Timer(get_task_name_updater(client), interval).start()
    macos_app.run()


if __name__ == '__main__':
    cli()
