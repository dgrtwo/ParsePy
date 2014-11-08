#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import mimetypes

from parse_rest.connection import API_ROOT
from parse_rest.datatypes import ParseBase, ParseType


class File(ParseBase, ParseType):
    ENDPOINT_ROOT = '/'.join([API_ROOT, 'files'])

    @classmethod
    def from_native(cls, **kw):
        f = cls(kw['name'])
        f._url = '/'.join([cls.ENDPOINT_ROOT, f.name])

    def __init__(self, name, content=None, mimetype=None):
        if isinstance(name, dict):
            name = name["name"]
        self._name = name
        self._url = None
        self._content = content
        self._mimetype = mimetype or mimetypes.guess_type(name)
        if not content:
            with open(name) as f:
                content = f.read()
        self._content = content

    def __repr__(self):
        return '<File:%s>' % (getattr(self, '_name', None))

    def _to_native(self):
        return {
            '__type': 'File',
            'name': self._name,
        }

    def save(self, batch=False):
        uri = '/'.join([self.__class__.ENDPOINT_ROOT, self.name])
        headers = {'Content-type': self.mimetype}
        response = self.__class__.POST(uri, extra_headers=headers, batch=batch, body=self._content)
        self._url = response['url']
        self._name = response['name']

        if batch:
            return response, lambda response_dict: None

    def delete(self, batch=False):
        uri = "/".join(self.__class__.ENDPOINT_ROOT, self.name)
        response = self.__class__.DELETE(uri, batch=batch)

        if batch:
            return response, lambda response_dict: None

    @property
    def name(self):
        return self._name

    @property
    def mimetype(self):
        return self._mimetype

    @property
    def url(self):
        return self._url
