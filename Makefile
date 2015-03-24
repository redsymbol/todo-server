test: unittest inttest_local
unittest:
	PYTHONPATH=$(shell pwd)/test:$$PYTHONPATH python -m unittest test_todoserver
inttest_local:
	PYTHONPATH=$(shell pwd)/test:$$PYTHONPATH python -m unittest test_todoserver_int_local
inttest_vm:
	PYTHONPATH=$(shell pwd)/test:$$PYTHONPATH python -m unittest test_todoserver_int_vm
