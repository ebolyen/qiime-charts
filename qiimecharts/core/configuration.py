import json
from qcerrors import ConfigError
from importlib import import_module
import csv
from source import Source
from mapping import Mapping
from qchart import get_chart
from biom.parse import parse_biom_table

class Configuration(object):

    def __init__(self, configing):
        self.config = json.loads(configing)
        self._build_sources()
        self._load_colors()
        self._load_strata()
        self._load_graphs()

    def __run__(self):
        return [get_chart(graph) for graph in self.graphs]

    def _build_sources(self):
        if 'sources' not in self.config:
            raise ConfigError('No sources in configuration')
        self.sources = {}
        for key, value in self.config['sources'].iteritems():
            name = key
            f = open(value['mapping'], 'U')
            mapping = Mapping(mapping_file_object=f)
            f.close()
            
            biom = None
            restrict = None
            if 'biom' in value:
                f = open(value['biom'], 'U')
                biom = parse_biom_table(f)
                f.close()

            if 'restrict' in value:
                restrict = (value['restrict']['column'], value['restrict']['values'])

            self.sources[key] = Source(name, mapping, biom=biom, restrict=restrict)

    def _load_colors(self):
        self.colors = {}
        if 'colors' in self.config:
            self.colors = self.config['colors']

    def _load_strata(self):
        if 'stratifications' not in self.config:
            raise ConfigError("No stratifications in configuration")

        def handle(s):
            if s['color'][:1] != "#":
                s['color'] = self.colors[s['color']]
            return s

        self.stratifications = {}
        for key, value in self.config['stratifications'].iteritems():
            self.stratifications[key] = [handle(x) for x in value]

    def _load_graphs(self):
        if 'graphs' not in self.config:
            raise ConfigError("No graphs in configuration")

        def recursive_link(l, p):
            for item in l:
                if isinstance(item, dict):
                    for key, value in item.iteritems():
                        if isinstance(value, unicode) and value.split(' ')[0] == '@var':
                            item[key] = p[value]
                        if key == 'y_stratification':
                            item[key] = self.stratifications[value]
                        elif key == 'x_stratification':
                            item[key] = self.stratifications[value]
                        elif key == 'source':
                            item[key] = self.sources[value]
                        elif key == 'data':
                            if isinstance(value, list):
                                item[key] = recursive_link(value, item)
                            else:
                                item[key] = recursive_link([value], item)

            return l

        self.graphs = recursive_link(self.config['graphs'], self.config)


