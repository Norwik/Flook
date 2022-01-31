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

from oranda.module.logger import Logger
from oranda.module.database import Database
from oranda.module.output import Output
from oranda.module.config import Config


class Hosts:
    """Hosts Class"""

    def __init__(self):
        self.output = Output()
        self.database = Database()
        self.config = Config()
        self.logger = Logger().get_logger(__name__)

    def init(self):
        """Init database and configs"""
        self._configs = self.config.load()
        self.database.connect(self._configs["database"]["path"])
        self.database.migrate()
        return self

    def add(self, name, configs):
        """Add a new host"""
        configs['ssh_private_key_file'] = configs["ssh_private_key_file"].read()

        if self.database.get_host(name) is not None:
            raise click.ClickException(f'Host with name {name} exists')

        self.database.insert_host(name, configs)
        click.echo(f'Host with name {name} got created')

    def list(self, tag, output):
        """List hosts"""
        data = []
        result = self.database.list_hosts()

        for item in result:
            data.append({
                "Name": item["name"],
                "Host": item["config"]["host"],
                "Connection": item["config"]["connection"].upper(),
                "Tags": ", ".join(item["config"]["tag"]) if len(item["config"]["tag"]) > 0 else "-"
            })

        print(self.output.render(data, Output.JSON if output.lower() == "json" else Output.DEFAULT))

    def get(self, name, output):
        """Get a host"""
        result = self.database.get_host(name)

        if result is None:
            raise click.ClickException(f'Host with name {name} not found')

        data = [{
            "Name": name,
            "Host": result["host"],
            "Connection": result["connection"].upper(),
            "Tags": ", ".join(result["tag"]) if len(result["tag"]) > 0 else "-"
        }]

        print(self.output.render(data, Output.JSON if output.lower() == "json" else Output.DEFAULT))

    def delete(self, name):
        """Delete a host"""
        self.database.delete_host(name)
        click.echo(f'Host with name {name} got deleted')