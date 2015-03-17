test: unittest inttest
unittest:
	PYTHONPATH=$(shell pwd)/test:$$PYTHONPATH python -m unittest test_todoserver
inttest:
	PYTHONPATH=$(shell pwd)/test:$$PYTHONPATH python -m unittest test_todoserver_int
