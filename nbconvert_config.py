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


c = get_config()

c.NbConvertApp.export_format = 'html'
c.NbConvertApp.output_files_dir = '../../assets/imgs/{notebook_name}'

c.HTMLExporter.preprocessors = [
	'nbconvert.preprocessors.ExecutePreprocessor',
	'nbconvert.preprocessors.coalesce_streams',
	'nbconvert.preprocessors.ExtractOutputPreprocessor']
c.HTMLExporter.template_file = 'notebooks/jekyll.tpl'
c.HTMLExporter.filters = {"jekyllimgurl": jekyllurl, "svg_filter": svg_filter}

c.ExecutePreprocessor.allow_errors = True

c.FilesWriter.build_directory = "_includes/notebooks/"
