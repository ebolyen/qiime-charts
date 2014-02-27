#!/usr/bin/env python
from __future__ import division

__credits__ = ["Evan Bolyen"]

from pyqi.core.command import (Command, CommandIn, CommandOut, 
    ParameterCollection)
from qiimecharts.core.configuration import Configuration

class RunConfiguration(Command):
    BriefDescription = "Generate charts from a configuration"
    LongDescription = "Generate charts from a configuration"

    CommandIns = ParameterCollection([
        CommandIn(Name='config', DataType=str,
                  Description='Configuration', Required=True)
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name='result', DataType=list,
                   Description='the resulting matplotlib plots')])

    def run(self, **kwargs):
        t = Configuration(kwargs['config'])
        x = t.__run__()
        return {'result': x}

CommandConstructor = RunConfiguration
