PYTHON ?= python3
NODE ?= node
NPM ?= npm

.PHONY: help install install-pdf test lint build verify pdf epub release check-all clean

help:
	@echo "Quantum Computing Handbook — Unified Build & QA Targets"
	@echo "  make install      Install locked Node/Playwright dependencies for tools/reader"
	@echo "  make install-pdf  Install locked Python PDF post-processing dependencies"
	@echo "  make test         Run offline stdlib experiments, vendor SHA-256 & WAV checks"
	@echo "  make lint         Run V4 quality, privacy, QM examples/review & network gates"
	@echo "  make build        Build offline HTML reader into reader/"
	@echo "  make verify       Run dual-viewport Playwright browser verification"
	@echo "  make pdf          Build A4 print-grade PDF into dist/quantum-computing-handbook.pdf"
	@echo "  make epub         Build native MathML 3 EPUB 3 into dist/quantum-computing-handbook.epub"
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

lint:
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

release: build verify pdf epub
	$(NODE) tools/reader/build-release.mjs $(if $(VERSION),--version $(VERSION),)

check-all: test lint build verify

clean:
	rm -rf dist/release _pages
	find . \( -path './.git' -o -path '*/vendor' -o -path './tools/reader/node_modules' \) -prune -o -type d -name '__pycache__' -prune -exec rm -rf {} +
