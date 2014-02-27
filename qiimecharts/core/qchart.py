import groupers as gp
from charts.bar import StackedBar, Bar

def stacked_bar(name, data, y_stratification,
                title=None,
                scaled=True,
                legend=True, **kwargs):
    x_labels = []
    bar_data = []
    for dp in data:
        x_labels.append(dp['display'])
        source = dp['source']
        grouper = gp.get_grouper(dp)

        column_totals = source.column_totals(dp['column'])

        totals = {}
        for key, value in column_totals.iteritems():
            if grouper(key) in totals:
                totals[grouper(key)] += value
            else:
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
                      legend=legend,
                      title=title, **kwargs)

def bar(name, data, x_stratification, title=None, **kwargs):
    data = data[0]
    source = data['source']

    aliases = {}
    x_labels = []
    colors = []
    for x in x_stratification:
        aliases[x['name']] = x['name']

    grouper = gp.get_grouper(data)
    column_totals = source.column_totals(data['column'])

    bar_data = []

    totals = {}
    for key, value in column_totals.iteritems():
        if grouper(key) in totals:
            totals[grouper(key)] += value
        else:
            totals[grouper(key)] = value

    for x in x_stratification:
        x_labels.append(x['display'])
        colors.append(x['color'])
        if x['name'] in totals:
            bar_data.append(totals[x['name']])
        else:
            bar_data.append(0)

    return Bar(name, bar_data, 
               x_labels=x_labels, 
               colors=colors, 
               title=title, **kwargs)

def get_chart(graph):
    return {
        'stackedbar': lambda : stacked_bar(graph['name'],
                                            graph['data'],
                                            graph['y_stratification'],
                                            title=(None if 'title' not in graph else graph['title']),
                                            dimension=(None if 'dimension' not in graph else graph['dimension']),
                                            scaled=(None if 'scaled' not in graph else graph['scaled']),
                                            legend_size=(None if 'legend_size' not in graph else graph['legend_size']),
                                            legend=(None if 'legend' not in graph else graph['legend'])),
        'bar': lambda : bar(graph['name'],
                            graph['data'],
                            graph['x_stratification'],
                            dimension=(None if 'dimension' not in graph else graph['dimension']),
                            title=(None if 'title' not in graph else graph['title']))
    }[graph['type']]()