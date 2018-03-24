"""CLI/Commands - List objects."""
from __future__ import absolute_import, print_function, unicode_literals

import click
from click_spinner import spinner

from . import main
from .push import wait_for_package_sync
from .. import decorators, validators
from ...core.api.packages import move_package
from ..exceptions import handle_api_exceptions


@main.command(aliases=['mv', 'promote'])
@decorators.common_api_auth_options
@decorators.common_cli_config_options
@decorators.common_cli_output_options
@decorators.common_package_action_options
@decorators.initialise_api
@click.argument(
    'owner_repo_package',
    metavar='OWNER/REPO/PACKAGE',
    callback=validators.validate_owner_repo_package)
@click.argument(
    'destination',
    metavar='DEST')
@click.pass_context
def move(
        ctx, opts, owner_repo_package, destination, skip_errors, wait_interval,
        no_wait_for_sync):
    """
    Move/promote a package to another repository.

    This requires appropriate permissions for both the source
    repository/package and the destination repository.

    - OWNER/REPO/PACKAGE: Specify the OWNER namespace (i.e. user or org), the
    REPO name where the package is stored, and the PACKAGE name (slug) of the
    package itself. All separated by a slash.

      Example: 'your-org/awesome-repo/better-pkg'.

    - DEST: Specify the DEST (destination) repository to move the package to.
    This *must* be in the same namespace as the source repository.

      Example: 'other-repo'

    Full CLI example:

      $ cloudsmith mv your-org/awesome-repo/better-pkg other-repo
    """
    owner, source, slug = owner_repo_package

    click.echo(
        'Moving %(slug)s package from %(source)s to %(dest)s ... ' % {
            'slug': click.style(slug, bold=True),
            'source': click.style(source, bold=True),
            'dest': click.style(destination, bold=True),
        }, nl=False
    )

    context_msg = 'Failed to move package!'
    with handle_api_exceptions(ctx, opts=opts, context_msg=context_msg,
                               reraise_on_error=skip_errors):
        with spinner():
            new_slug_perm, new_slug = move_package(
                owner=owner,
                repo=source,
                slug=slug,
                destination=destination
            )

    click.secho('OK', fg='green')

    if no_wait_for_sync:
        return

    wait_for_package_sync(
        ctx=ctx, opts=opts, owner=owner, repo=destination, slug=new_slug,
        wait_interval=wait_interval, skip_errors=skip_errors
    )