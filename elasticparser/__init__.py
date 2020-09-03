# Copyright 2015-2018 Lauri Himanen, Fawzi Mohamed, Ankit Kariryaa
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from .metainfo import m_env
from nomad.parsing.parser import FairdiParser
from elasticparser.elastic_parser import ElasticParserInterface


class ElasticParser(FairdiParser):
    def __init__(self):
        super().__init__(
            name='parsers/elastic', code_name='elastic', code_homepage='http://exciting-code.org/elastic',
            mainfile_contents_re=r'\s*Order of elastic constants\s*=\s*[0-9]+\s*',
            mainfile_name_re=(r'.*/INFO_ElaStic'))

    def parse(self, filepath, archive, logger=None):
        self._metainfo_env = m_env

        parser = ElasticParserInterface(filepath, archive, logger)

        parser.parse()
