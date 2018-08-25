from nbconvert.preprocessors import ExecutePreprocessor, Preprocessor
import numpy as np


def jekyllurl(path):
    """
    Take the filepath of an image output by the ExportOutputProcessor
    and convert it into a URL we can use with Jekyll
    """
    return path.replace("../..", "")


def svg_filter(svg_xml):
    """
    Remove the DOCTYPE and XML version lines from
    the inline XML SVG
    """
    svgstr = "".join(svg_xml)
    start_index = svgstr.index("<svg")
    end_index = svgstr.index("</svg>")
    return svgstr[start_index:end_index + 6]


def var_def_to_var_list(var_def):
    if 'linspace' in var_def:
        v = var_def.replace("linspace(", "")
        v = v.replace(")", "")
        start, stop, num = v.split(",")
        return np.linspace(
            float(start.strip()),
            float(stop.strip()),
            float(num.strip()))
    elif '[' in var_def and ']' in var_def:
        v = var_def.replace("[", "")
        v = v.replace("]", "")
        v = v.split(",")
        return [x.strip() for x in v]
    else:
        raise TypeError("not implemented for {}".format(var_def))


class ExecuteWithInteractPreprocessor(ExecutePreprocessor):
    def preprocess_cell(self, cell, resources, cell_index):
        if cell.cell_type != 'code':
            return cell, resources

        if "@manipulate" in cell.source:
            original_source = cell.source

            cell_manipulate = cell.copy()
            cell_source = original_source.split("\n")
            cell_manipulate.source = "\n".join([cell_source[0], cell_source[-1]])
            manipulate_output = self.run_cell(cell_manipulate)
            outs = []
            outs.extend(manipulate_output)

            main_source = "\n".join(cell_source[1:-1])
            var_def = cell_source[0].replace("@manipulate", "")
            var_def = var_def.replace("for", "").strip().split("=")
            var_name, var_list = var_def
            # currently this only works for a single for loop
            # turn all the variables into a loop
            all_vars = var_def_to_var_list(var_list)
            for next_var in all_vars:
                var_defs = "{}={}".format(var_name, next_var)
                cell_copy = cell.copy()
                cell_copy.source = "\n".join([var_defs, main_source.strip()])
                outputs = self.run_cell(cell_copy)
                outs.extend(outputs)

            cell.source = original_source
            cell.outputs = outs

            # fix the outputs
            # probably better done at the postprocessing step
            # import ipdb; ipdb.set_trace()
            # raise TypeError("stopping")
        else:
            outputs = self.run_cell(cell)
            cell.outputs = outputs

        return cell, resources

            # if 'Interact' in cell.outputs[0]['data']['text/plain']:
                # there should be a widget here


class RemoveInteractJsShimPreprocessor(Preprocessor):
    def preprocess(self, nb, resources):
        """
        make sure the widgets resources get put into the resources
        """
        if 'widgets' in nb['metadata'].keys():
            resources['metadata']['widgets'] = nb['metadata']['widgets']
        return super(RemoveInteractJsShimPreprocessor, self).preprocess(nb, resources)

    def preprocess_cell(self, cell, resources, cell_index):
        """
        remove any outputs that have interact-js-shim
        """
        if 'outputs' in cell:
            outputs = cell['outputs']
            new_outputs = []
            for output in outputs:
                new_output = output.copy()
                if "data" in output.keys():
                    data_output = output["data"]
                    new_data_output = data_output.copy()
                    if 'text/html' in data_output.keys():
                        text_html = data_output['text/html']
                        if text_html.startswith('<div id=\"interact-js-shim\">'):
                            start_index = text_html.find('<div id=\"interact-js-shim\">')
                            end_index = text_html.find('</div>')
                            new_html = ""
                            if start_index > 0:
                                new_html += text_html[0:start_index]
                            if end_index + 6 < len(text_html):
                                new_html += text_html[end_index+6:]
                            new_html = new_html.strip()
                            if len(new_html) > 0:
                                new_data_output['text/html'] = new_html
                            else:
                                del new_data_output['text/html']
                        else:
                            new_data_output['text/html'] = text_html
                    if len(new_data_output.keys()) > 0:
                        new_output['data'] = new_data_output
                    else:
                        del new_output['data']
                    if 'data' in new_output:
                        new_outputs.append(new_output)
                else:
                    new_outputs.append(new_output)
            cell['outputs'] = new_outputs
        return cell, resources


class InsertWidgetsPreprocessor(Preprocessor):

    def preprocess_cell(self, cell, resources, cell_index):
        """
        if the cell is a cell with @manipulate, add the appropriate
        widget script into the output 
        """
        if cell.cell_type != 'code':
            return cell, resources

        if "@manipulate" in cell.source:
            widget_state = resources['metadata']['widgets']['application/vnd.jupyter.widget-state+json']['state']
            interact_options = cell.outputs[0]['data']['text/plain']
            start_index = interact_options.find('"')
            model_name = interact_options[start_index + 1:]
            next_index = model_name.find('"')
            model_name = model_name[:next_index]
            # match the widget based on the descriptions
            matched_model_id = None
            for model_id in widget_state.keys():
                if widget_state[model_id]['state']['description'] == model_name:
                    matched_model_id = model_id
                    break
            # construct the script tag
            script_tag = '<script type="application/vnd.jupyter.widget-view+json">{"model_id": "' + matched_model_id + '"}</script>'
            cell.outputs[0]['data']['text/html'] = script_tag

        return cell, resources

c = get_config()

c.NbConvertApp.export_format = 'html'
c.NbConvertApp.output_files_dir = '../../assets/imgs/{notebook_name}'

c.HTMLExporter.preprocessors = [
    'nbconvert.preprocessors.ExecutePreprocessor',
    # ExecuteWithInteractPreprocessor,
    'nbconvert.preprocessors.coalesce_streams',
    'nbconvert.preprocessors.ExtractOutputPreprocessor',
    RemoveInteractJsShimPreprocessor,
    InsertWidgetsPreprocessor]
c.HTMLExporter.template_file = 'notebooks/jekyll.tpl'
c.HTMLExporter.filters = {"jekyllimgurl": jekyllurl, "svg_filter": svg_filter}

# if there's an error in one of the cells let the execution keep going
c.ExecutePreprocessor.allow_errors = True
# disable the timeout
c.ExecutePreprocessor.timeout = -1
c.ExecutePreprocessor.iopub_timeout = 10

# write the final HTML files into the _include/notebooks directory
c.FilesWriter.build_directory = "_includes/notebooks/"
