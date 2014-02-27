import groupers as gp
from charts.bar import StackedBar

def stacked_bar(name, data, y_stratification,
                title=None,
                scaled=True,
                legend=True):
    x_labels = []
    bar_data = []
    for dp in data:
        x_labels.append(dp['display'])
        source = dp['source']
        grouper = gp.get_grouper(dp)

        column_totals = source.column_totals(dp['column'])

        totals = {}
        for key, value in column_totals.iteritems():
            totals[grouper(key)] = value

        colors = []
        y_labels = []
        bar = []
        for y in y_stratification:
            y_labels.insert(0, y['display'])
            colors.insert(0, y['color'])
            if y['name'] in totals:
                bar.insert(0, totals[y['name']])
            else:
                bar.insert(0, 0)
        bar_data.append(bar)

    return StackedBar(name, bar_data, 
                      scaled=scaled,
                      x_labels=x_labels,
                      y_labels=y_labels,
                      colors=colors,
                      legend=legend)

def get_chart(graph):
    return {
        'stackedbar': lambda : stacked_bar(graph['name'],
                                            graph['data'],
                                            graph['y_stratification'],
                                            title=(None if 'title' not in graph else graph['title']),
                                            scaled=(None if 'scaled' not in graph else graph['scaled']),
                                            legend=(None if 'legend' not in graph else graph['legend']))
    }[graph['type']]()