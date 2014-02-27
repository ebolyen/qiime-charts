#!/usr/bin/env python

__credits__ = ["Evan Bolyen"]

def write_list_of_figures(result_key, data, option_value=None):
    for chart in data:
        chart.save()