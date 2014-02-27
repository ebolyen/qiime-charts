from qiimecharts.core.charts.base import Chart
import matplotlib.pyplot as plt
#from qiimecharts.core.colors.default import ColorGen as default_colors

class StackedBar(Chart):

	def __init__(self, name, data, scaled=True, **kwargs):
		super(StackedBar, self).__init__(name, **kwargs)
		n_data = data
		if not scaled:
			n_data = denormalize(n_data)
		n_data = invert(n_data)

		ind, width = self._even_spacing_factory(len(data), self.padding)

		if 'x_labels' in kwargs:
			if scaled:
				self.plot.set_xticklabels(kwargs['x_labels'])
			else:
				self.plot.set_xticklabels([label + " (n=%d)" % sum(data[i]) for i, label in enumerate(kwargs['x_labels'])])


		self.plot.set_xticks(ind)
		self.plot.set_xlim([min(ind) - (0.75 * width), max(ind) + (0.75 * width)])

		bottom = 0
		bars = []
		for observation_data in n_data:
			bar = self.plot.bar(ind, observation_data, width, 
						  color=self.colors.next(),
						  bottom=bottom, 
						  align='center',
						  linewidth=0)
			bars.append(bar)
			if bottom == 0:
				bottom = observation_data
			else:
				bottom = add_lists_pairwise(bottom, observation_data)

		if 'legend' in kwargs and kwargs['legend']:
			if not ('legend_outside' in kwargs and kwargs['legend_outside']):
				legend = self.plot.legend(bars[::-1], kwargs['y_labels'][::-1], loc='best', fancybox=True)
				legend.get_frame().set_alpha(0.5)
			else:
				self.plot.legend(bars[::-1], kwargs['y_labels'][::-1], loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True)



class Bar(StackedBar):

	def __init__(self, name, data, normalized=True, y_stratification=None, **kwargs):
		pass



def denormalize(data):
	return [[float(e)/sum(v) for e in v] for v in data]

def add_lists_pairwise(l1, l2):
	return [sum(x) for x in zip(l1, l2)]

def invert(data):
	n_data = []
	for i in range(0, len(data[0])):
		n_data.append([l[i] for l in data])
	return n_data
