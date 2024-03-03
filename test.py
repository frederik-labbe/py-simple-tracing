from tracing import TracingModule

def f(x, y, z):
	if (type(x).__name__ != 'int' or type(y).__name__ != 'int' or type(z).__name__ != 'int'):
		raise ValueError('Invalid parameters !')
	
	print(x + y + z)

def my_function(x, y):
	f(x, y, 6)

if __name__ == '__main__':
	TracingModule().enable(
		log_function=print,
		included_files=[__file__],
		show_variables=True,
		monitored_variables=['z'])
	
	n = 2
	x = n + 3
	
	my_function(2, 4)
	
	my_function(True, 1)
	
	#print(__file__)
