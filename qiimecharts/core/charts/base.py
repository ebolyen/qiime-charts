
from matplotlib import use
use('Agg')
import matplotlib.pyplot as plt


class Chart(object):
    def __init__(self, name, transparent=False, **kwargs):
        self.elements = []
        self.transparent = transparent
        self.name = name

        self._fig = plt.figure(figsize=kwargs.get('dimension', (4, 3.5)),
                               dpi=kwargs.get('dpi', 80))

        self._fig.canvas.manager.set_window_title(name)
        self.plot = self._fig.add_subplot(1, 1, 1)

        if 'title' in kwargs:
            self._fig.suptitle(kwargs['title'], fontsize=20)

        if 'y_label' in kwargs:
            self.plot.set_ylabel(kwargs['y_label'])

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
                loc = kwargs.get('legend_loc', None)
                legend_size = kwargs.get('legend_size', None)
                y_labels = kwargs.get('y_labels', [])
                if 'legend_size' in kwargs:
                    legend = self.plot.legend(self.elements[::-1],
                                              y_labels[::-1],
                                              loc=loc, fancybox=True,
                                              prop={'size': legend_size})
                else:
                    legend = self.plot.legend(self.elements[::-1],
                                              y_labels[::-1],
                                              loc=loc,
                                              fancybox=True)
                legend.get_frame().set_alpha(0.5)
                if 'changer' in kwargs:
                    kwargs['changer'](legend)

            else:
                raise Exception("'legend_outside' is not yet implemented")
                self.plot.legend(self.elements[::-1], kwargs['y_labels'][::-1], loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, prop={'size':kwargs['legend_size']})

    def save(self, path=''):
        self._fig.tight_layout()
        self._fig.subplots_adjust(top=0.85)
        self._fig.savefig(path+self.name + self.format, format=self.format, transparent=self.transparent)

    def show(self):
        self._fig.tight_layout()
        self._fig.subplots_adjust(top=0.85)
        self._fig.show()
