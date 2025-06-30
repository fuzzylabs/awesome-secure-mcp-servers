# Makefile for Awesome Secure MCP Servers

.PHONY: all discover process scan update report validate test test-validation

# Configuration
PYTHON = python3
SCRIPTS_DIR = scripts
DATA_DIR = data
REPORTS_DIR = security

# Files
SERVERS_DATA = $(DATA_DIR)/servers.json
DISCOVERED_SERVERS = $(DATA_DIR)/discovered-servers.json
PROCESSED_SERVERS = $(DATA_DIR)/processed-servers.json
SCAN_RESULTS = $(REPORTS_DIR)/scan-results.json
REPORT = $(REPORTS_DIR)/report.md
README = README.md

all: validate discover process scan update report

validate:
	@echo "Validating data..."
	$(PYTHON) $(SCRIPTS_DIR)/validate.py --data $(SERVERS_DATA)

discover:
	@echo "Discovering new servers..."
	$(PYTHON) $(SCRIPTS_DIR)/server-discovery.py --output $(DISCOVERED_SERVERS)

process:
	@echo "Processing discovered servers..."
	$(PYTHON) $(SCRIPTS_DIR)/process-discovered-servers.py --discovered $(DISCOVERED_SERVERS) --existing $(SERVERS_DATA) --output $(PROCESSED_SERVERS)

scan:
	@echo "Scanning servers..."
	$(PYTHON) $(SCRIPTS_DIR)/security-scanner.py --input $(SERVERS_DATA) --output $(SCAN_RESULTS)

update:
	@echo "Updating data and README..."
	$(PYTHON) $(SCRIPTS_DIR)/update-artifacts.py --servers $(SERVERS_DATA) --scan-results $(SCAN_RESULTS) --readme $(README)

report:
	@echo "Generating report..."
	$(PYTHON) $(SCRIPTS_DIR)/generate-report.py --scan-results $(SCAN_RESULTS) --output $(REPORT)

test:
	@echo "Running tests..."
	$(PYTHON) test_runner.py

test-validation:
	@echo "Running validation tests..."
	$(PYTHON) -m unittest tests.test_validate -v

clean:
	@echo "Cleaning up generated files..."
	rm -f $(DISCOVERED_SERVERS) $(PROCESSED_SERVERS) $(SCAN_RESULTS) $(REPORT)
