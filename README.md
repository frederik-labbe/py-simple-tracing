# py-simple-tracing

## Control options

| **Name**            | **Description**                                                                                                     |
|---------------------|---------------------------------------------------------------------------------------------------------------------|
| included_files      | Files to be included in the tracing. When specified, only those files will be traced.                               |
| show_variables      | Whether or not to show variables for each step.                                                                     |
| monitored_variables | List of variables to be monitored. When specified, steps need to have at least one of these variables to be traced. |

## Output options

| **Name**                  | **Description**                               |
|---------------------------|-----------------------------------------------|
| log_function              | Function to be used for logging a trace, default otherwise.      |
| output_exception_function | Function to be used for tracing an exception, default otherwise. |
| output_line_function      | Function to be used for tracing a line, default otherwise.       |
| output_call_function      | Function to be used for tracing a call, default otherwise.       |

## Code sample

```python
from tracing import TracingModule

TracingModule().enable(
		log_function=print,
		included_files=[__file__],
		show_variables=True,
		monitored_variables=['z'])
```

## Sample trace
```
Entering function f
*  with variables {'x': 2, 'y': 4, 'z': 6}
*  on line 3 of /home/fred/Projects/tracing_test/test.py
*  from line 10 of /home/fred/Projects/tracing_test/test.py
Executing line 4 --> 	if (type(x).__name__ != 'int' or type(y).__name__ != 'int' or type(z).__name__ != 'int'):
*  with variables {'x': 2, 'y': 4, 'z': 6}
*  of /home/fred/Projects/tracing_test/test.py
Executing line 7 --> 	print(x + y + z)
*  with variables {'x': 2, 'y': 4, 'z': 6}
*  of /home/fred/Projects/tracing_test/test.py
12
Entering function f
*  with variables {'x': True, 'y': 1, 'z': 6}
*  on line 3 of /home/fred/Projects/tracing_test/test.py
*  from line 10 of /home/fred/Projects/tracing_test/test.py
Executing line 4 --> 	if (type(x).__name__ != 'int' or type(y).__name__ != 'int' or type(z).__name__ != 'int'):
*  with variables {'x': True, 'y': 1, 'z': 6}
*  of /home/fred/Projects/tracing_test/test.py
Executing line 5 --> 		raise ValueError('Invalid parameters !')
*  with variables {'x': True, 'y': 1, 'z': 6}
*  of /home/fred/Projects/tracing_test/test.py
Exception at line 5 --> 		raise ValueError('Invalid parameters !')
*  with variables {'x': True, 'y': 1, 'z': 6}
*  of /home/fred/Projects/tracing_test/test.py
```
