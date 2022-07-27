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
    manage_case = 0x1

    manage_users = 0x10
    read_users = 0x20

    manage_customers = 0x40
    read_customers = 0x80

    manage_case_objects = 0x100
    read_case_objects = 0x200

    manage_modules = 0x400
    read_modules = 0x800

    manage_custom_attributes = 0x1000
    read_custom_attributes = 0x2000

    manage_templates = 0x4000

    manage_server_settings = 0x8000
    read_server_settings = 0x10000

    manage_own_organisation = 0x20000
    manage_organisations = 0x40000

    manage_groups = 0x80000

    read_all_activities = 0x100000
    read_all_dim_tasks = 0x200000

    search_across_cases = 0x400000
    search_across_all_cases = 0x8000000