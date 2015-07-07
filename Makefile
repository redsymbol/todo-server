test:
	PYTHONPATH=$(shell pwd)/src:$(shell pwd)/test:$$PYTHONPATH python -m unittest test_todoserver

.PHONY: test
