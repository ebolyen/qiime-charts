from qiimecharts.core.charts.base import Chart
import matplotlib.pyplot as plt

class Pie(Chart):

    def __init__(self, name, data, **kwargs):
        super(Pie, self).__init__(name, **kwargs)

        self.plot.pie(data, colors=kwargs['colors'])
        raise Exception("Not ready")

        self._load_legend(changer=self._legend_changer(), **kwargs)

    def _legend_changer(self):
        pass