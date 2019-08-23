from derex.runner.plugins import setup_plugin_manager
from pathlib import Path
from derex.runner.docker import create_deps
from derex.runner.plugins import Registry
from typing import List, Optional, Union
from compose.cli.main import main
import click
import os
import re
import hashlib
import pkg_resources
import sys
import yaml
import derex


def run_compose(
    args: List[str],
    variant: str = "services",
    dry_run: bool = False,
    project: Optional["derex.runner.project.Project"] = None,
):
    create_deps()

    plugin_manager = setup_plugin_manager()
    registry = Registry()
    if project:
        for opts in plugin_manager.hook.local_compose_options(project=project):
            registry.add(
                key=opts["name"], value=opts["options"], location=opts["priority"]
            )
    else:
        for opts in plugin_manager.hook.compose_options():
            if opts["variant"] == variant:
                registry.add(
                    key=opts["name"], value=opts["options"], location=opts["priority"]
                )
    settings = [el for lst in registry for el in lst]
    old_argv = sys.argv
    try:
        sys.argv = ["docker-compose"] + settings + args
        if not dry_run:
            click.echo(f'Running {" ".join(sys.argv)}')
            main()
        else:
            click.echo("Would have run")
            click.echo(click.style(" ".join(sys.argv), fg="blue"))
    finally:
        sys.argv = old_argv
