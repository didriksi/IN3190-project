### Makefile based on one created for a project in FYS3150 Computational Physics ###


### List of all plots and data used directly in project.tex ###
PLOTS = plots/map.pdf plots/distances.pdf plots/fir.pdf plots/freq_spec.pdf plots/sections.pdf plots/arrival_times.pdf

### Files used for compiling latex ###
TEX_FILES = $(wildcard latex/*.tex)
PYTHON_FILES = $(wildcard src/*.py)
PLOT_PYTHON_FILES = src/main.py src/plot.py

### Python runner ###
PYTHON ?= python3

### Raw files already present ###
RAW_FILES = $(wildcard data/raw/*)

### Compile pdf from LaTeX ###
report.pdf: $(PLOTS) $(TEX_FILES) $(PYTHON_FILES)
	cd latex && pdflatex report && biber report && pdflatex report && pdflatex report
	mv latex/report.pdf report.pdf

preview: $(TEX_FILES)
	cd latex && latexmk -pdf -pvc report.tex

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
tasks/make_folder_structure:
	mkdir tasks
	mkdir plots
	mkdir data/raw
	mkdir data/processed
	mkdir data/processed/convolved
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/make_folder_structure

tasks/venv: requirements.txt
	pip install --upgrade pip
	$(PYTHON) -m venv venv
	source venv/bin/activate; pip install -r requirements.txt
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/venv

tasks/unzip: tasks/make_folder_structure
ifeq ($(strip $(RAW_FILES)),)
	cd data/raw/ && unzip ../../project_data.zip
endif
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/unzip

tasks/parse_data: tasks/make_folder_structure tasks/venv tasks/unzip data src/process_data.py
	source venv/bin/activate; python src/main.py --parse-data
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/parse_data

tasks/plot_map: tasks/parse_data tasks/venv $(PLOT_PYTHON_FILES)
	source venv/bin/activate; python src/main.py --plot-map
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/plot_map

tasks/plot_distances: tasks/parse_data tasks/venv $(PLOT_PYTHON_FILES)
	source venv/bin/activate; python src/main.py --plot-distances
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/plot_distances

tasks/plot_fir: tasks/parse_data tasks/venv $(PLOT_PYTHON_FILES)
	source venv/bin/activate; python src/main.py --plot-fir
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/plot_fir

tasks/plot_frequency_spectrum: tasks/parse_data tasks/venv $(PLOT_PYTHON_FILES)
	source venv/bin/activate; python src/main.py --plot-freq-spec
	echo "Completed at" $$(date +%Y-%m/%d_%H:%M:%S) > tasks/plot_frequency_spectrum

tasks/filter_signals: tasks/parse_data tasks/venv
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

### Plots needed for the report ###
plots/map.pdf: tasks/plot_map

plots/distances.pdf: tasks/plot_distances

plots/fir.pdf: tasks/plot_fir

plots/freq_spec.pdf: tasks/plot_frequency_spectrum

plots/sections.pdf: tasks/plot_sections

plots/arrival_times.pdf: tasks/plot_arrival_time

