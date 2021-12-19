test:
	@echo Running unit tests.
	@python3 -m doctest main.py && echo All unit tests passed!
	@echo
	@echo Running examples.py. Expected output is "1 2 3" several times.
	@python3 main.py examples.py | python3
