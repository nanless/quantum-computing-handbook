PYTHON ?= python3
NODE ?= node
NPM ?= npm
JAVA ?= java
EPUBCHECK ?= epubcheck

.PHONY: help install install-pdf test lint build verify pdf epub check-epub release release-verify release-epub-check check-all clean

help:
	@echo "Quantum Computing Handbook — Unified Build & QA Targets"
	@echo "  make install      Install locked Node/Playwright dependencies for tools/reader"
	@echo "  make install-pdf  Install locked Python PDF post-processing dependencies"
	@echo "  make test         Run offline stdlib experiments and vendor SHA-256 checks"
	@echo "  make lint         Run V4 quality, privacy, QM examples/review & network gates"
	@echo "  make build        Build offline HTML reader into reader/"
	@echo "  make verify       Run Playwright at 1440, 390 and 320px browser verification"
	@echo "  make pdf          Build A4 print-grade PDF into dist/quantum-computing-handbook.pdf"
	@echo "  make epub         Build native MathML 3 EPUB 3 into dist/quantum-computing-handbook.epub"
	@echo "  make check-epub   Run EPUBCheck; set EPUBCHECK_JAR to use an official JAR"
	@echo "  make release      Build web/PDF/EPUB and package dist/release/ suite with SHA256SUMS (optional VERSION=v1.0.0)"
	@echo "  make check-all    Run test + lint + build + verify"
	@echo "  make clean        Remove temporary staging outputs (dist/release/, _pages/) and non-vendor __pycache__/"

install:
	$(NPM) ci --prefix tools/reader --ignore-scripts --no-audit --no-fund
	$(NPM) exec --prefix tools/reader -- playwright install chromium

install-pdf:
	$(PYTHON) -m pip install -r tools/reader/requirements-pdf.txt

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) codes/run_all.py
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) codes/tests/test_validation_entrypoints.py

lint:
	$(NODE) --test tools/reader/exercise-identity.test.mjs tools/reader/epub-mathml.test.mjs tools/reader/build-provenance.test.mjs tools/reader/reading-order.test.mjs
	$(NODE) tools/reader/check-v3-quality.mjs
	$(NODE) tools/reader/check-qm-examples.mjs
	$(NODE) tools/reader/check-qm-review.mjs
	$(NODE) tools/reader/check-network-examples.mjs

build:
	$(NODE) tools/reader/build.mjs

verify:
	$(NODE) tools/reader/verify.mjs

pdf:
	PYTHONDONTWRITEBYTECODE=1 $(NODE) tools/reader/build-pdf.mjs

epub:
	PYTHONDONTWRITEBYTECODE=1 $(NODE) tools/reader/build-epub.mjs

release-verify: build
	$(MAKE) verify

release-epub-check: epub
	$(MAKE) check-epub

release: release-verify pdf release-epub-check
	$(NODE) tools/reader/build-release.mjs $(if $(VERSION),--version $(VERSION),)
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) tools/reader/release-publish.py suite --version $(if $(VERSION),$(VERSION),v1.0.0)

check-epub:
	$(if $(EPUBCHECK_JAR),$(JAVA) -jar "$(EPUBCHECK_JAR)",$(EPUBCHECK)) dist/quantum-computing-handbook.epub --failonwarnings

check-all: test lint build
	$(MAKE) verify

clean:
	rm -rf dist/release _pages
	find . \( -path './.git' -o -path '*/vendor' -o -path './tools/reader/node_modules' \) -prune -o -type d -name '__pycache__' -prune -exec rm -rf {} +
