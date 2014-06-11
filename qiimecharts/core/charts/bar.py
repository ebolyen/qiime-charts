from qiimecharts.core.charts.base import Chart
import matplotlib.pyplot as plt

class StackedBar(Chart):

    def __init__(self, name, data, scaled=True, **kwargs):
        super(StackedBar, self).__init__(name, **kwargs)
        n_data = data
        if not scaled:
            n_data = denormalize(n_data)
        n_data = invert(n_data)

        ind, width = self._even_spacing_factory(len(data), self.padding)
        rot = kwargs.get('x_label_rotation', 90)
        ha = kwargs.get('x_labels_alignment', 'center')

        if 'x_labels' in kwargs:
            if scaled:
                self.plot.set_xticklabels(kwargs['x_labels'], rotation=rot, ha=ha)
            else:
                self.plot.set_xticklabels([label + " (n=%d)" % kwargs['n_values'][i] for i, label in enumerate(kwargs['x_labels'])],
                                          rotation=rot, ha=ha)


        self.plot.set_xticks(ind)
        self.plot.set_xlim([min(ind) - (0.75 * width), max(ind) + (0.75 * width)])

        bottom = 0
        self.elements = []
        for observation_data in n_data:
            bar = self.plot.bar(ind, observation_data, width,
                          color=self.colors.next(),
                          bottom=bottom,
                          align='center',
                          linewidth=0)
            self.elements.append(bar)
            if bottom == 0:
                bottom = observation_data
            else:
                bottom = add_lists_pairwise(bottom, observation_data)

        self._load_legend(**kwargs)




class Bar(StackedBar):

    def __init__(self, name, data, **kwargs):
        super(Bar, self).__init__(name, self._psuedo_stack(data), **kwargs)

    def _psuedo_stack(self, data):
        stacked = []
        for i, bar in enumerate(data):
            stacked.append([0 for x in range(len(data))])
            stacked[i][i] = bar
        return stacked



def denormalize(data):
    return [[float(e)/sum(v) for e in v] for v in data]

def add_lists_pairwise(l1, l2):
    return [sum(x) for x in zip(l1, l2)]

def invert(data):
    n_data = []
    for i in range(0, len(data[0])):
        n_data.append([l[i] for l in data])
    return n_data
