
.PHONY: test
test:
	pytest . --cov . --cov-branch --cov-report term-missing
