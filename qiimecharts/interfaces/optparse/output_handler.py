#!/usr/bin/env python

__credits__ = ["Evan Bolyen"]

def write_list_of_figures(result_key, data, option_value=None):
    for chart in data:
        chart['figure'].savefig(option_value + chart['name'] + '.png', format='png', bbox_inches='tight')