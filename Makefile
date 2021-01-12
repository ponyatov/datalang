# \ <section:var>
MODULE       = $(notdir $(CURDIR))
OS           = $(shell uname -s)
MACHINE      = $(shell uname -m)
NOW          = $(shell date +%d%m%y)
REL          = $(shell git rev-parse --short=4 HEAD)
# / <section:var>
# \ <section:dir>
CWD          = $(CURDIR)
DOC          = $(CWD)/doc
BIN          = $(CWD)/bin
SRC          = $(CWD)/src
TMP          = $(CWD)/tmp
# / <section:dir>
# \ <section:tool>
WGET         = wget -c
CURL         = curl
PY           = $(BIN)/python3
PIP          = $(BIN)/pip3
PEP          = $(BIN)/autopep8
PYT          = $(BIN)/pytest
# / <section:tool>
# \ <section:obj>
P   += $(MODULE).py config.py
# / <section:obj>
S   += $(P) $(C) $(H) $(R) $(E) $(X) $(L)
# \ <section:all>
.PHONY: all
all: $(PY) $(MODULE).py	
	# \ <section:body>
	$^
	# / <section:body>
.PHONY: repl
repl: $(PY) $(MODULE).py
	clear
	$(PY) -i $(MODULE).py
	$(MAKE) $@
.PHONY: pep
pep: $(PEP)
$(PEP): $(P)
	$(PEP) --ignore=E26,E302,E401,E402 --in-place $? && touch $@
# / <section:all>
# \ <section:doc>
.PHONY: doc
doc:  

# / <section:doc>
# \ <section:gz>
.PHONY: gz
gz:
# / <section:gz>
# \ <section:install>
.PHONY: install
install: $(OS)_install
	$(MAKE) gz
	$(MAKE) doc
	# \ <section:body>
	$(MAKE) $(PIP)
	$(MAKE) update
	# / <section:body>
.PHONY: update
update: $(OS)_update
	# \ <section:update>
	$(PIP)  install -U pip autopep8
	$(PIP)  install -U -r requirements.pip
	# / <section:update>
.PHONY: $(OS)_install $(OS)_update
$(OS)_install $(OS)_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`
# \ <section:pyinst>
$(PY) $(PIP):
	python3 -m venv .
	$(MAKE) update
$(PYT):
	$(PIP) install pytest
# / <section:pyinst>
# / <section:install>
# \ <section:merge>
MERGE  = Makefile README.md apt.txt .gitignore .vscode $(S)
.PHONY: main
main:
	git push -v
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)
.PHONY: shadow
shadow:
	git push -v
	git checkout $@
	git pull -v
.PHONY: release
release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow
.PHONY: zip
zip:
	git archive \
		--format zip \
		--output $(TMP)/$(MODULE)_$(NOW)_$(REL).src.zip \
	HEAD
# / <section:merge>
