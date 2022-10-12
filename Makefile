### Makefile based on one created for a project in FYS3150 Computational Physics ###


### List of all plots and data used directly in project.tex ###
TASKS = tasks/validation tasks/burn-in

### Files used for compiling latex ###
TEX_FILES = $(wildcard latex/*.tex)

### Python runner ###
PYTHON ?= python3

### Creating folders ###
plots:
	mkdir plots

### Managing virtual python environment ###
venv:
	$(PYTHON) -m venv venv
	(source venv/bin/activate)
	pip install -r requirements.txt

.PHONY: activate_venv
activate_venv: venv
	(source venv/bin/activate)

### Compile pdf from LaTeX ###
project.pdf: $(TASKS) $(TEX_FILES)
	cd latex && pdflatex report.tex
	mv latex/report.pdf report.pdf

preview: $(TEX_FILES)
	cd latex && latexmk -pdf -pvc main.tex

### General commands ###
.PHONY: all
all: test clean project.pdf

.PHONY: clean
clean:
	@echo "Deleting compiled files and the folders containing them"
	@rm -f latex/report.pdf
	@rm -f -rf plots
	@rm -f -rf venv
	@rm -f -rf src/__pycache__
	@rm -f latex/report.log
	@rm -f latex/report.aux
	@rm -f latex/texput.log
	@rm -f latex/report.out
	@rm -f latex/report.bbl
	@rm -f latex/report.blg
	@rm -f latex/reportNotes.bib
	@rm -f latex/amsmath.aux
	@rm -f latex/report.fdb_latexmk
	@rm -f latex/report.fls

### Tasks ###
tasks/parse_data:
	python src/main.py --parse-data
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/parse_data
