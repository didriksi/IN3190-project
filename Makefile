### Makefile based on one created for a project in FYS3150 Computational Physics ###


### List of all plots and data used directly in project.tex ###
TASKS = tasks/venv tasks/unzip tasks/parse_data tasks/plot_map tasks/plot_distances tasks/plot_fir tasks/plot_frequency_spectrum tasks/filter_signals

### Files used for compiling latex ###
TEX_FILES = $(wildcard latex/*.tex)
PYTHON_FILES = $(wildcard src/*.py)
PLOT_PYTHON_FILES = src/main.py src/plot.py

### Python runner ###
PYTHON ?= python3

### Raw files already present ###
RAW_FILES = $(wildcard data/raw/*)

### Creating folders ###
tasks:
	mkdir tasks

plots:
	mkdir plots

data:
	mkdir data/raw
	mkdir data/processed
	mkdir data/processed/convolved

### Compile pdf from LaTeX ###
report.pdf: $(TASKS) $(TEX_FILES) $(PYTHON_FILES)
	cd latex && pdflatex report.tex
	mv latex/report.pdf report.pdf

preview: $(TEX_FILES)
	cd latex && latexmk -pdf -pvc main.tex

### General commands ###
.PHONY: all
all: clean report.pdf

.PHONY: clean
clean:
	@echo "Deleting compiled files and the folders containing them"
	@rm -f report.pdf
	@rm -f -rf plots
	@rm -f -rf venv
	@rm -f -rf data/raw
	@rm -f -rf data/processed
	@rm -f -rf tasks
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
tasks/venv: tasks requirements.txt
	pip install --upgrade pip
	$(PYTHON) -m venv venv
	source venv/bin/activate; pip install -r requirements.txt
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/venv

tasks/unzip: tasks data
ifeq ($(strip $(RAW_FILES)),)
	cd data/raw/ && unzip ../../project_data.zip
endif
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/unzip

tasks/parse_data: tasks tasks/venv tasks/unzip data src/process_data.py
	source venv/bin/activate; python src/main.py --parse-data
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/parse_data

tasks/plot_map: tasks/parse_data tasks/venv plots $(PLOT_PYTHON_FILES)
	source venv/bin/activate; python src/main.py --plot-map
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/plot_map

tasks/plot_distances: tasks/parse_data tasks/venv plots $(PLOT_PYTHON_FILES)
	source venv/bin/activate; python src/main.py --plot-distances
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/plot_distances

tasks/plot_fir: tasks/parse_data tasks/venv plots $(PLOT_PYTHON_FILES)
	source venv/bin/activate; python src/main.py --plot-fir
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/plot_fir

tasks/plot_frequency_spectrum: tasks/parse_data tasks/venv plots $(PLOT_PYTHON_FILES)
	source venv/bin/activate; python src/main.py --plot-freq-spec
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/plot_frequency_spectrum

tasks/filter_signals: data tasks/parse_data tasks/venv
	source venv/bin/activate; python src/main.py --filter-signals
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/filter_signals

tasks/plot_sections: tasks/parse_data tasks/filter_signals tasks/venv $(PLOT_PYTHON_FILES)
	source venv/bin/activate; python src/main.py --plot-sections
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/plot_sections

tasks/mark_arrival_time: tasks/parse_data tasks/filter_signals tasks/venv $(PLOT_PYTHON_FILES)
	source venv/bin/activate; python src/main.py --mark-arrival-times
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/mark_arrival_time

tasks/plot_arrival_time: tasks/parse_data tasks/filter_signals tasks/venv $(PLOT_PYTHON_FILES)
	source venv/bin/activate; python src/main.py --plot-arrival-times
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/plot_arrival_time
