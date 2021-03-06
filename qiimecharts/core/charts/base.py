
from matplotlib import use
use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class Chart(object):
    _graph_sets_written = set()

    def __init__(self, name, transparent=False, **kwargs):
        if 'graph_set' in kwargs:
            gs = kwargs['graph_set']
            self._graph_set = id(gs)
            gs_rows, gs_cols = gs['subplot_shape']
            rows, cols = kwargs.get('dimension', (gs_rows, 2))

            if '_gs' not in gs:
                gs['figure'] = plt.figure()
                gs['_gs'] = gridspec.GridSpec(gs_rows, gs_cols)
                gs['subplot_offset'] = 0

            self._fig = gs['figure']

            so = gs['subplot_offset']
            gs['subplot_offset'] += cols

            self.plot = self._fig.add_subplot(gs['_gs'][:, so:so+cols])
        else:
            self._fig = plt.figure(figsize=kwargs.get('dimension', (4, 3.5)),
                                   dpi=kwargs.get('dpi', 80))
            self._fig.canvas.manager.set_window_title(name)
            self.plot = self._fig.add_subplot(1, 1, 1)
            self._graph_set = None

        self.elements = []
        self.transparent = transparent
        self.name = name

        self._ax = plt.gca()

        self.xylabel_family = kwargs.get('font_family', None)
        self.xylabel_size = kwargs.get('fontsize', None)

        if 'ylim' in kwargs:
            self.plot.set_ylim(kwargs['ylim'])

        if 'xgrid' in kwargs and kwargs['xgrid']:
            self.plot.axes.xaxis.grid(True)

        if 'ygrid' in kwargs and kwargs['ygrid']:
            self.plot.axes.yaxis.grid(True)

        if 'y_ticks' in kwargs and not kwargs['y_ticks']:
            self.plot.axes.get_yaxis().set_ticklabels([''])

        if 'title' in kwargs:
            self.plot.set_title(kwargs['title'], fontsize=self.xylabel_size)

        if 'y_label' in kwargs:
            self.plot.set_ylabel(kwargs['y_label'], fontsize=self.xylabel_size)

        if 'x_padding' in kwargs:
            self.padding = kwargs['x_padding']
        else:
            self.padding = 0.5

        self.format = kwargs.get('format', 'png')

        if 'colors' not in kwargs:
            raise Exception("COLORS")
        self.colors = self._color_gen(kwargs['colors'])

    def _color_gen(self, color_list):
        while True:
            for color in color_list:
                yield color

    def _even_spacing_factory(self, count, x_padding):
        if x_padding > 0:
            width = 1/x_padding
        else:
            width = 1

        def indent_gen():
            last = 1
            while True:
                yield last
                last += width + 1
        i = indent_gen()
        # This feels weird, but I don't have time to care. Will come back to this to refactor.
        return ([i.next() for _ in range(count)], width)

    def _load_legend(self, **kwargs):
        if 'legend' in kwargs and kwargs['legend']:
            if not ('legend_outside' in kwargs and kwargs['legend_outside']):
                legend = None
                loc = kwargs.get('legend_loc', 'best')
                legend_size = kwargs.get('legend_size', None)
                y_labels = kwargs.get('y_labels', [])
                font_family = kwargs.get('font_family', None)

                if 'legend_size' in kwargs:
                    legend = self.plot.legend(self.elements[::-1],
                                              y_labels[::-1],
                                              loc=loc, fancybox=True,
                                              prop={'size': legend_size,
                                                    'family': font_family})
                else:
                    legend = self.plot.legend(self.elements[::-1],
                                              y_labels[::-1],
                                              loc=loc,
                                              fancybox=True,
                                              prop={'family': font_family})
                if 'changer' in kwargs:
                    kwargs['changer'](legend)

            else:
                raise Exception("'legend_outside' is not yet implemented")
                self.plot.legend(self.elements[::-1], kwargs['y_labels'][::-1], loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, prop={'size':kwargs['legend_size']})

    def _finalize(self):
        for label in self._ax.get_yticklabels() + self._ax.get_xticklabels():
            label.set_fontsize(self.xylabel_size)
            label.set_family(self.xylabel_family)
        self._fig.tight_layout()
        self._fig.subplots_adjust(top=0.85)

    def save(self, path=''):
        if self._graph_set is None:
            self._finalize()
            self._fig.savefig(path+ self.name + '.' + self.format, format=self.format, transparent=self.transparent)
        else:
            if self._graph_set not in Chart._graph_sets_written:
                Chart._graph_sets_written.add(self._graph_set)
                self._finalize()
                self._fig.savefig(path+ self.name + '.' + self.format, format=self.format, transparent=self.transparent)

    def show(self):
        self._finalize()
        self._fig.show()
