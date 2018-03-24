"""CLI/Commands - List objects."""
from __future__ import absolute_import, print_function, unicode_literals

import click
from click_spinner import spinner

from . import main
from .push import wait_for_package_sync
from .. import decorators, validators
from ...core.api.packages import resync_package
from ..exceptions import handle_api_exceptions


@main.command()
@decorators.common_api_auth_options
@decorators.common_cli_config_options
@decorators.common_cli_output_options
@decorators.common_package_action_options
@decorators.initialise_api
@click.argument(
    'owner_repo_package',
    metavar='OWNER/REPO/PACKAGE',
    callback=validators.validate_owner_repo_package)
@click.pass_context
def resync(
        ctx, opts, owner_repo_package, skip_errors, wait_interval,
        no_wait_for_sync):
    """
    Resynchronise a package in a repository.

    This requires appropriate permissions for package.

    - OWNER/REPO/PACKAGE: Specify the OWNER namespace (i.e. user or org), the
    REPO name where the package is stored, and the PACKAGE name (slug) of the
    package itself. All separated by a slash.

      Example: 'your-org/awesome-repo/better-pkg'.

    Full CLI example:

      $ cloudsmith resync your-org/awesome-repo/better-pkg
    """
    owner, source, slug = owner_repo_package

    click.echo(
        'Resynchonising the %(slug)s package ... ' % {
            'slug': click.style(slug, bold=True)
        }, nl=False
    )

    context_msg = 'Failed to resynchronise package!'
    with handle_api_exceptions(ctx, opts=opts, context_msg=context_msg,
                               reraise_on_error=skip_errors):
        with spinner():
            resync_package(
                owner=owner,
                repo=source,
                slug=slug
            )

    click.secho('OK', fg='green')

    if no_wait_for_sync:
        return

    wait_for_package_sync(
        ctx=ctx, opts=opts, owner=owner, repo=source, slug=slug,
        wait_interval=wait_interval, skip_errors=skip_errors
    )