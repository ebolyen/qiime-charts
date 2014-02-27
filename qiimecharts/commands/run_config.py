#!/usr/bin/env python
from __future__ import division

__credits__ = ["Evan Bolyen"]

from pyqi.core.command import (Command, CommandIn, CommandOut, 
    ParameterCollection)

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
        
        return {'result': []}

CommandConstructor = RunConfiguration
