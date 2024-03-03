import sys


def default_log(*txt):
	print(*txt)


def default_output_line(**out):
	log_function = out.get('log_function')
	line_number = out.get('line_number')
	line = out.get('line')
	show_variables = out.get('show_variables')
	variables = out.get('variables')
	func_filename = out.get('func_filename')
	
	log_function(f'Executing line {line_number} --> {line}')
	
	if show_variables:
		log_function(f'*  with variables {variables}')
	
	log_function(f'*  of {func_filename}')


def default_output_exception(**out):
	log_function = out.get('log_function')
	line_number = out.get('line_number')
	line = out.get('line')
	show_variables = out.get('show_variables')
	variables = out.get('variables')
	func_filename = out.get('func_filename')
	
	log_function(f'Exception at line {line_number} --> {line}')

	if show_variables:
		log_function(f'*  with variables {variables}')
	
	log_function(f'*  of {func_filename}')


def default_output_function_call(**out):
	log_function = out.get('log_function')
	func_name = out.get('func_name')
	line_number = out.get('line_number')
	func_filename = out.get('func_filename')
	show_variables = out.get('show_variables')
	variables = out.get('variables')
	caller_line_number = out.get('caller_line_number')
	caller_filename = out.get('caller_filename')
	
	log_function(f'Entering function {func_name}')
	
	if show_variables:
		log_function(f'*  with variables {variables}')
	
	log_function(f'*  on line {line_number} of {func_filename}')
	
	if caller_line_number is not None and caller_filename is not None:
		log_function(f'*  from line {caller_line_number} of {caller_filename}')


class TracingModule:
	def __init__(self):
		self._included_files = None
		self._show_variables = False
		self._monitored_variables = None

		self._fc_log = None
		self._fc_output_line = None
		self._fc_output_exception = None
		self._fc_output_function_call = None

		self._dict_file_lines = dict()

	def _read_options(self, **options):
		# Control options
		
		included_files = options.get('included_files')
		show_variables = options.get('show_variables')
		monitored_variables = options.get('monitored_variables')
		
		if included_files is not None:
			if not isinstance(included_files, list):
				raise ValueError('Included files need to be a list.')

			self._included_files = included_files
			
		if show_variables is not None:
			if not isinstance(show_variables, bool):
				raise ValueError('Option "Show Variables" needs to be a bool.')

			self._show_variables = show_variables
			
		if monitored_variables is not None:
			if not isinstance(monitored_variables, list):
				raise ValueError('Monitored variables need to be a list.')
				
			if not show_variables:
				raise ValueError('You need to activate option "Show Variables" to monitor variables.')

			self._monitored_variables = monitored_variables
		
		# Output functions
		
		log_function = options.get('log_function')
		if log_function is None:
			log_function = default_log
		if not callable(log_function):
			raise ValueError('Log function needs to be callable.')
		self._fc_log = log_function
		
		output_exception_function = options.get('output_exception_function')
		if output_exception_function is None:
			output_exception_function = default_output_exception
		if not callable(output_exception_function):
			raise ValueError('Function for exception output needs to be callable.')
		self._fc_output_exception = output_exception_function
			
		output_line_function = options.get('output_line_function')
		if output_line_function is None:
			output_line_function = default_output_line
		if not callable(output_line_function):
			raise ValueError('Function for line output needs to be callable.')
		self._fc_output_line = output_line_function
			
		output_call_function = options.get('output_call_function')
		if output_call_function is None:
			output_call_function = default_output_function_call
		if not callable(output_call_function):
			raise ValueError('Function for call output needs to be callable.')
		self._fc_output_function_call = output_call_function


	def _trace_lines(self, frame, event, arg):
		variables = frame.f_locals

		if self._monitored_variables is not None and not any([v in self._monitored_variables for v in variables]):
			return
			
		co = frame.f_code
		
		line_number = frame.f_lineno
		func_filename = co.co_filename

		file_lines = self._dict_file_lines.get(func_filename)
		if not file_lines:
			with open(func_filename, 'r') as f:
				file_lines = self._dict_file_lines[func_filename] = f.read().splitlines()
				
		line = file_lines[line_number - 1]
			
		out = {
			'log_function': self._fc_log,
			'line_number': line_number,
			'line': line,
			'show_variables': self._show_variables,
			'variables': variables,
			'func_filename': func_filename }

		if event == 'line':	
			self._fc_output_line(**out)
		
		if event == 'exception':
			self._fc_output_exception(**out)
		
		return
	
	def _trace_calls(self, frame, event, arg):
		co = frame.f_code
		func_name = co.co_name
		
		if func_name == 'write':
			# Ignore write() calls from printing
			return
			
		line_number = frame.f_lineno
		func_filename = co.co_filename

		if self._included_files is not None and func_filename not in self._included_files:
			return
			
		variables = frame.f_locals
		
		if self._monitored_variables is not None and not any([v in self._monitored_variables for v in variables]):
			return
			
		out = {
			'log_function': self._fc_log,
			'func_name': func_name,
			'line_number': line_number,
			'func_filename': func_filename,
			'show_variables': self._show_variables,
			'variables': variables
		}
		
		caller = frame.f_back
		
		if caller is not None:
			caller_line_number = caller.f_lineno
			caller_filename = caller.f_code.co_filename
			
			out['caller_line_number'] = caller_line_number
			out['caller_filename'] = caller_filename

		self._fc_output_function_call(**out)

		return self._trace_lines
	
	
	def enable(self, **options):
		self._read_options(**options)
		sys.settrace(self._trace_calls)
