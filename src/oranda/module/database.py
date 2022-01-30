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

import json
import sqlite3


class Database():
    """Database Class"""

    def __init__(self, path):
        self.path = path

    def connect(self):
        """Connect into a database"""
        self._connection = sqlite3.connect(self.path)
        return self._connection.total_changes

    def migrate(self):
        cursor = self._connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS host (name TEXT, config TEXT)")

        cursor.close()
        self._connection.commit()

    def delete(self, host):
        """Delete a row by host name"""
        cursor = self._connection.cursor()

        cursor.execute(
            "DELETE FROM host WHERE name = ?",
            (host,)
        )

        cursor.close()
        self._connection.commit()

    def get(self, host):
        """Get a row by host name"""
        cursor = self._connection.cursor()

        rows = cursor.execute("SELECT name, config FROM host WHERE name = '{}'".format(host)).fetchall()

        cursor.close()

        if len(rows) > 0:
            return json.loads(rows[0][1])
        else:
            return None

    def insert(self, host, configs={}):
        """Insert a new row"""
        cursor = self._connection.cursor()

        result = cursor.execute("INSERT INTO host VALUES ('{}', '{}')".format(
            host,
            json.dumps(configs)
        ))

        cursor.close()
        self._connection.commit()
        return result.rowcount

    def list(self):
        """List all rows"""
        result = []

        cursor = self._connection.cursor()
        rows = cursor.execute("SELECT name, config FROM host").fetchall()
        cursor.close()

        for row in rows:
            result.append({
                "name": row[0],
                "config": json.loads(row[1])
            })

        return result