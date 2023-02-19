#  IRIS Client API Source Code
#  contact@dfir-iris.org
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#  Based on https://github.com/airbus-cyber/iris-httpsend-module/blob/main/tests/docker_compose.py
#
import subprocess
from pathlib import Path
import logging as log


class DockerHelper(object):

    def __init__(self, docker_compose_path: str) -> None:

        self._compose_file = docker_compose_path
        if not Path(self._compose_file).exists():
            raise FileNotFoundError(f"File {self._compose_file} does not exist")

    def _run_command(self, command: str) -> None:
        """Runs a docker-compose command"""
        command = f"docker-compose -f {self._compose_file} {command}"
        log.info(f"Running command: {command}")

        subprocess.run(command, check=True, shell=True)

    def start(self) -> None:
        """Starts the docker-compose environment"""
        self._run_command("up -d")

    def stop(self) -> None:
        """Stops the docker-compose environment"""
        self._run_command("logs")
        self._run_command("down --volumes")
