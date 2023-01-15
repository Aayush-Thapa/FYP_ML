#!/bin/python3
# author: Nisha Pela
# mail: nisha.pela@pathao.com 

import nbformat
from nbparameterise import (
    extract_parameters, replace_definitions, parameter_values
)
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
    
def final_func(file_name, user_):
    # read source notebook
    with open(file_name) as f:
        nb = nbformat.read(f, as_version=4)

    # Get a list of Parameter objects
    orig_parameters = extract_parameters(nb)

    # Update one or more parameters
    params = parameter_values(orig_parameters, u = user_)
    new_nb = replace_definitions(nb, params)
    print('userr is ', user_)
    print()
    # execute notebook
    ep = ExecutePreprocessor(timeout=-1, kernel_name='python3')
    ep.preprocess(new_nb)

    # export to html
    html_exporter = HTMLExporter()
    html_exporter.exclude_input = True
    html_data, resources = html_exporter.from_notebook_node(new_nb)
    return html_data