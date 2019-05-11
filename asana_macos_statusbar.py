from typing import Optional

import click
import click_spinner
import rumps
from asana import Client
from asana.error import NoAuthorizationError

from asana_api import AsanaClient
from macos import macos_app, get_task_name_updater


@click.group()
def cli():
    """
    asana_macos_statusbar displays your current task in MacOS statusbar.
    """


@cli.command()
@click.argument('access_token')
def init(access_token: str):
    """
    Use this helper to get specific values from Asana API and choose the tasks you need.

    Before launch you should make or get access_token — https://asana.com/guide/help/api/api
    """
    client = Client.access_token(access_token)

    click.echo('Starting validation of access_token...')
    with click_spinner.spinner():
        try:
            user = client.users.me()
        except NoAuthorizationError:
            click.secho(
                'Token is invalid. Please check your token and read the ' +
                'official documentation: https://asana.com/guide/help/api/api',
                fg='red'
            )
            return
    click.echo('Hello, {0}'.format(user['name']))

    click.echo('Fetching workspaces...')
    with click_spinner.spinner():
        workspaces = list(client.workspaces.find_all())

    click.echo('Please choose workspace')
    for i, w in enumerate(workspaces, 1):
        click.echo('{index}: {name} ({gid})'.format(
            index=i,
            name=w['name'],
            gid=w['gid'],
        ))
    workspace_index = click.prompt('Your choice', type=int) - 1
    workspace = workspaces[workspace_index]

    click.echo('Selected workspace {name} ({gid})'.format(
        name=workspace['name'],
        gid=workspace['gid']
    ))

    filter_type = click.prompt(
        'You can use only one type of fetching tasks:\n' +
        '1. Show in status bar last task filtered by tag\n' +
        '2. Show in status bar last task filtered by project\n' +
        '3. Show in status bar last task filtered by column of board (so-called section)\n'
        'Your choice',
        type=int
    )

    if filter_type == 1:
        click.echo('Fetching tags...')
        with click_spinner.spinner():
            tags = list(client.tags.find_all(workspace=workspace['gid']))
        click.echo('Please choose tag')
        for i, t in enumerate(tags, 1):
            click.echo('{index}: {name} ({gid})'.format(
                index=i,
                name=t['name'],
                gid=t['gid'],
            ))
        tag_index = click.prompt('Your choice', type=int) - 1
        tag = tags[tag_index]

        click.secho('Use run command with "--tag-id {0}"'.format(tag['gid']), fg='green')
        return

    click.echo('Fetching projects...')
    with click_spinner.spinner():
        projects = list(client.projects.find_all(workspace=workspace['gid']))
    click.echo('Please choose project')
    for i, p in enumerate(projects, 1):
        click.echo('{index}: {name} ({gid})'.format(
            index=i,
            name=p['name'],
            gid=p['gid'],
        ))
    project_index = click.prompt('Your choice', type=int) - 1
    project = projects[project_index]

    if filter_type == 2:
        click.secho('Use run command with "--project-id {0}"'.format(project['gid']), fg='green')
        return

    if filter_type == 3:
        click.echo('Fetching sections...')
        with click_spinner.spinner():
            sections = list(client.sections.find_by_project(project=project['gid']))
        click.echo('Please choose column of board (section)')
        for i, s in enumerate(sections, 1):
            click.echo('{index}: {name} ({gid})'.format(
                index=i,
                name=s['name'],
                gid=s['gid'],
            ))
        section_index = click.prompt('Your choice', type=int) - 1
        section = sections[section_index]
        click.secho('Use run command with "--section-id {0}"'.format(section['gid']), fg='green')
        return


@cli.command()
@click.argument('access_token')
@click.option('--section-id', default=None)
@click.option('--tag-id', default=None)
@click.option('--project-id', default=None)
@click.option('--interval', default=60, show_default=True)
def run(access_token: str, section_id: Optional[str], tag_id: Optional[str], project_id: Optional[str], interval: int):
    """
    Run asana_macos_statusbar.

    Before launch you should make or get access_token — https://asana.com/guide/help/api/api

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
