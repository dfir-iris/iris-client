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

"""
Defines standard template types
"""
from enum import Enum


class ReportTemplateType(Enum):
    InvestigationReport = 1
    ActivityReport = 2


class ReportTemplateLanguage(Enum):
    french = 1
    english = 2
    german = 3
    bulgarian = 4
    croatian = 5
    danish = 6
    dutch = 7
    estonian = 8
    finnish = 9
    greek = 10
    hungarian = 11
    irish = 12
    italian = 13
    latvian = 14
    lithuanian = 15
    maltese = 16
    polish = 17
    portuguese = 18
    romanian = 19
    slovak = 20
    slovenian = 21
    spanish = 22
    swedish = 23
    indian = 24
    chinese = 25
    korean = 26
    arabic = 27
    japanese = 28
    turkish = 29
    vietnamese = 30
    thai = 31
    hebrew = 32
    czech = 33
    norwegian = 34
    brazilian = 35
    ukrainian = 36
    catalan = 37
    serbian = 38
    persian = 39
    afrikaans = 40
    albanian = 41


