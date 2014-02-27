#!/usr/bin/env python

__credits__ = ["Evan Bolyen"]

from pyqi.core.interfaces.optparse import (OptparseOption,
                                           OptparseResult,
                                           OptparseUsageExample)
from pyqi.core.interfaces.optparse.input_handler import load_file_contents
from qiimecharts.interfaces.optparse.output_handler import write_list_of_figures
from pyqi.core.command import (make_command_in_collection_lookup_f,
                               make_command_out_collection_lookup_f)
from qiimecharts.commands.run_config import CommandConstructor

cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

usage_examples = [
    OptparseUsageExample(ShortDesc="Create charts from config",
                         LongDesc="Create charts from config",
                         Ex='%prog -i config.json -o /some/directory')
]

inputs = [
    OptparseOption(Parameter=cmd_in_lookup('config'),
                   Handler=load_file_contents,
                   ShortName='i')
]

outputs = [
    ### InputName is used to tie this output to output-fp, which is an input...
    OptparseResult(Parameter=cmd_out_lookup('result'),
                   Handler=write_list_of_figures)
]
