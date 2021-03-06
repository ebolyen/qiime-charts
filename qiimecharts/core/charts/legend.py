from base import Chart
import matplotlib.pyplot as plt
import numpy as np

class Legend(Chart):
    def __init__(self, name, **kwargs):
        super(Legend, self).__init__(name, **kwargs)
        dummy_fig = plt.figure()
        dummy_axes = dummy_fig.gca()

        ind = range(len(kwargs['y_labels']))
        width = 1
        data = range(len(kwargs['y_labels']))
        font_family = kwargs.get('font_family', None)

        
        dummy = dummy_axes.bar(ind, data, width, color=[self.colors.next() for x in data])

        self.format = kwargs.get('format', 'png')

       # if 'dimension' in kwargs:
       #     self._fig = plt.figure(figsize=kwargs['dimension'], dpi=80,)
       # else:
       #     self._fig = plt.figure()

        if 'title' in kwargs:
            self._fig.suptitle(kwargs['title'], fontsize=20)

        if 'legend_size' in kwargs:
            legend = self.plot.legend(dummy[::-1], kwargs['y_labels'][::-1], fancybox=False, loc='center', prop={'size':kwargs['legend_size'],
                                                                                                                'family': font_family})
        else:
            legend = self.plot.legend(dummy[::-1], kwargs['y_labels'][::-1], fancybox=False)
        legend.draw_frame(False)
        dummy_fig.delaxes(dummy_axes)
        self.plot.axis('off')





    #def save(self, path=''):
    #    self._fig.savefig(path + self.name + '.' + self.format, format=self.format,
    #                      transparent=self.transparent)

    def show(self):
        self._fig.show()
