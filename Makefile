test: unittest inttest_bootstrap
unittest:
	PYTHONPATH=$(shell pwd)/test:$$PYTHONPATH python -m unittest test_todoserver
inttest_boostrap:
	PYTHONPATH=$(shell pwd)/test:$$PYTHONPATH python -m unittest test_todoserver_int_bootstrap
inttest_vm:
	PYTHONPATH=$(shell pwd)/test:$$PYTHONPATH python -m unittest test_todoserver_int_vm
