# -*- coding: utf-8 -*-
#########################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-TODAY Pseudo code. (<http://pseudocode.co>).

#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version. You can not redistribute or sale
#    without permission of Pseudo code. (<http://pseudocode.co>).

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################################
{
    'name': "Leave Reports",
    'summary': """Holiday and Leave Summary Reports""",
    'description': """
    """,
    "version": "11.0",
    "category": "Reports",
    'author': "Itara",
    "website": "http://www.itara.com",
    "application": False,
    'installable': True,
    "depends": [
        'base'],
    "data": [
        'views/gstr_return_view.xml',
    ],
}
