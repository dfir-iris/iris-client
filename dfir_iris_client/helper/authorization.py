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
import enum


class CaseAccessLevel(enum.Enum):
    deny_all = 0x1
    read_only = 0x2
    full_access = 0x4


class Permissions(enum.Enum):
    standard_user = 0x1
    server_administrator = 0x2

    alerts_read = 0x4
    alerts_write = 0x8
    alerts_delete = 0x10

    search_across_cases = 0x20

    customers_read = 0x40
    customers_write = 0x80

    case_templates_read = 0x100
    case_templates_write = 0x200

    activities_read = 0x400
    all_activities_read = 0x800