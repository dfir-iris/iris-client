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

class CaseOutcomeStatusHelper(object):
    """Handles the case outcome status API calls."""

    def __init__(self, session):
        """Initialize the class."""
        self._s = session

    def list_case_outcome_status_types(self):
        """
        List all case outcome status types.
        """
        return self._s.pi_get('/manage/outcome-status/list', cid=1)

    def lookup_case_outcome_status_name(self, case_outcome_status_name):
        """
        Lookup a case outcome status ID from its name.
        """
        cst_list = self.list_case_outcome_status_types()
        for ast in cst_list.get_data():
            if ast.get('name').lower() == case_outcome_status_name.lower():
                return ast.get('value')

        return None
