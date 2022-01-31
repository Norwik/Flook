# MIT License
#
# Copyright (c) 2023 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import click
import logging, json, sys
from oranda import __version__
from oranda.command.hosts import Hosts
from oranda.command.recipes import Recipes
from oranda.module.table import Table

@click.group(help="🐺 A Lightweight and Flexible Ansible Command Line Tool")
@click.version_option(version=__version__, help="Show the current version")
def main():
    pass

@click.group(help='Manage hosts')
def host():
    pass

@host.command(help='List hosts')
@click.option("-t", "--tag", "tag", type=click.STRING, default="", help="Host tags")
@click.option("-o", "--output", "output", type=click.STRING, default="", help="Output format")
def list(tag, output):
    Table().draw(["Host", "IP"], [["clivern.com", "127.0.0.1"]])
    Hosts().list(tag, output)

@host.command(help='Add a host')
@click.argument('name')
@click.option("-c", "--connection", "connection", type=click.STRING, default="ssh", help="Connection type to the host")
@click.option("-h", "--host", "host", type=click.STRING, default="", help="The name of the host to connect to")
@click.option("-p", "--port", "port", type=click.INT, default=22, help="The connection port number")
@click.option("-u", "--user", "user", type=click.STRING, default="root", help="The user name to use when connecting to the host")
@click.option("-pa", "--password", "password", type=click.STRING, default="", help="The password to use to authenticate to the host")
@click.option("-s", "--ssh_private_key_file", "ssh_private_key_file", type=click.File(), default="", help="Private key file used by ssh")
@click.option("-t", "--tag", "tag", type=click.STRING, default="", help="Host tags")
@click.option("-o", "--output", "output", type=click.STRING, default="", help="Output format")
def add(name, connection, host, port, user, password, ssh_private_key_file, tag, output):
    Hosts().add(name, {
        "connection": connection,
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "ssh_private_key_file": ssh_private_key_file,
        "tag": tag,
        "output": output
    })

@host.command(help='Get a host')
@click.argument('name')
@click.option("-o", "--output", "output", type=click.STRING, default="", help="Output format")
def get(name, output):
    Hosts().get(name, output)

@host.command(help='Delete a host')
def delete(name):
    Hosts().delete(name)


@click.group(help='Manage recipes')
def recipe():
    pass

@recipe.command(help='Add a recipe')
@click.argument('name')
@click.option("-p", "--path", "path", type=click.Path(exists=True), default="", help="Path to the recipe")
def add(name, path):
    Recipes().add(name, {
        "path": path
    })

@recipe.command(help='List all recipes')
@click.option("-t", "--tag", "tag", type=click.STRING, default="", help="Recipe tags")
@click.option("-o", "--output", "output", type=click.STRING, default="", help="Output format")
def list(tag, output):
    Recipes().list(tag, output)

@recipe.command(help='Get a recipe')
@click.argument('name')
@click.option("-o", "--output", "output", type=click.STRING, default="", help="Output format")
def get(name, output):
    Recipes().get(name, output)

@recipe.command(help='Delete a recipe')
def delete(name):
    Recipes().delete(name)

main.add_command(host)
main.add_command(recipe)

if __name__ == '__main__':
    main()
