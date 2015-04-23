test:
	PYTHONPATH=$(shell pwd)/test:$$PYTHONPATH python -m unittest test_todoserver

.PHONY: test
