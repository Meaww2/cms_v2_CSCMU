#!/usr/bin/env python3


# Contest Management System - http://cms-dev.github.io/
# Copyright © 2016-2018 Stefano Maggiolo <s.maggiolo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Racket programming language, version 3, definition."""
import os

from cms.grading import CompiledLanguage


__all__ = ["Racket"]


class Racket(CompiledLanguage):
    """This defines the Racket programming language, version 18 (more
    precisely, the subversion of Racket available on the system)
    using the default interpeter in the system.

    """

    MAIN_FILENAME = "main.rkt"

    @property
    def name(self):
        """See Language.name."""
        return "Racket"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".rkt"]

    @property
    def requires_multithreading(self):
        """See Language.requires_multithreading."""
        return True

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        commands = []
        # commands.append(["/usr/bin/raco", "exe", "--3m", "--orig-exe", "-o",
        #                  executable_filename, source_filenames[0]])

        zip_filename = "%s.zip" % executable_filename
        files_to_package = []
        # commands.append(["/usr/bin/python3.8", "-m", "compileall", "-b", "."])
        for idx, source_filename in enumerate(source_filenames):
            basename = os.path.splitext(os.path.basename(source_filename))[0]
            rkt_filename = "%s.rkt" % basename
            # The file with the entry point must be in first position.
            if idx == 0:
                commands.append(["/bin/mv", rkt_filename, self.MAIN_FILENAME])
                files_to_package.append(self.MAIN_FILENAME)
            else:
                files_to_package.append(rkt_filename)

        # zip does not support writing to a file without extension.
        commands.append(["/usr/bin/zip", "-r", zip_filename]
                        + files_to_package)
        commands.append(["/bin/mv", zip_filename, executable_filename])

        return commands

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        commands = []
        zip_filename = "%s.zip" % executable_filename
        commands.append(["/bin/mv", executable_filename, zip_filename])
        commands.append(["/usr/bin/unzip", zip_filename])
        commands.append(["/usr/bin/rm", zip_filename])
        commands.append(["/usr/bin/racket", self.MAIN_FILENAME])
        return commands