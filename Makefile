.PHONY: docx-list docx-validate docx-render-all docx-render-one vale-bootstrap

PYTHON ?= python3
TOOLKIT_DIR ?= ../dac-toolkit
MANIFEST ?= manifests/render-manifest.yaml
DOC_ID ?=
KROKI_URL ?= http://127.0.0.1:8000

docx-list:
	$(PYTHON) $(TOOLKIT_DIR)/scripts/docx_manifest.py list --content-root . --manifest "$(MANIFEST)"

docx-validate:
	$(PYTHON) $(TOOLKIT_DIR)/scripts/docx_manifest.py validate --content-root . --manifest "$(MANIFEST)"

docx-render-all:
	$(PYTHON) $(TOOLKIT_DIR)/scripts/docx_manifest.py render --content-root . --manifest "$(MANIFEST)" --kroki-url "$(KROKI_URL)"

docx-render-one:
	$(PYTHON) $(TOOLKIT_DIR)/scripts/docx_manifest.py render --content-root . --manifest "$(MANIFEST)" --document-id "$(DOC_ID)" --kroki-url "$(KROKI_URL)"

vale-bootstrap:
	bash $(TOOLKIT_DIR)/scripts/vale-bootstrap.sh

