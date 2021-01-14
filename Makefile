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
P   += $(MODULE).py test_$(MODULE).py
# / <section:obj>
S   += $(P) $(C) $(H) $(R) $(E) $(X) $(L)
# \ <section:all>
.PHONY: all
all: $(PY) $(MODULE).py	
	$^ $@
.PHONY: web
web: $(PY) $(MODULE).py	
	$^ $@
.PHONY: test
test: $(PYT) test_$(MODULE).py
	$^
.PHONY: repl
repl: $(PY) $(MODULE).py
	clear
	$(PY) -i $(MODULE).py $@
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
	$(MAKE) js
	$(MAKE) $(PY) $(MODULE).py
	$(PY) $(MODULE).py $@
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
# \ <section:js>
.PHONY: js
js: \
	static/jquery.js \
	static/bootstrap.css static/bootstrap.js \
	static/html5shiv.js static/respond.js \
	static/leaflet.css static/leaflet.js

JQUERY_VER = 3.5.1
JQUERY_JS  = https://code.jquery.com/jquery-$(JQUERY_VER).js
static/jquery.js:
	$(WGET) -O $@ $(JQUERY_JS)

BOOTSTRAP_VER = 3.4.1
static/bootstrap.css:
	$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.css
static/bootstrap.js:
	$(WGET) -O $@ https://maxcdn.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/js/bootstrap.js

HTML5SHIV_VER = 3.7.3
HTML5SHIV_URL = https://cdnjs.cloudflare.com/ajax/libs/html5shiv/$(HTML5SHIV_VER)/html5shiv-printshiv.js
static/html5shiv.js:
	$(WGET) -O $@ $(HTML5SHIV_URL)

RESPOND_VER = 1.4.2
RESPOND_URL = https://cdnjs.cloudflare.com/ajax/libs/respond.js/$(RESPOND_VER)/respond.js
static/respond.js:
	$(WGET) -O $@ $(RESPOND_URL)

LEAFLET_VER = 1.7.1
LEAFLET_ZIP = http://cdn.leafletjs.com/leaflet/v$(LEAFLET_VER)/leaflet.zip
$(TMP)/leaflet.zip:
	$(WGET) -O $@ $(LEAFLET_ZIP)
static/leaflet.css: static/leaflet.js
static/leaflet.js: $(TMP)/leaflet.zip
	unzip -d static $< leaflet.css leaflet.js* images/* && touch $@
# / <section:js>
# / <section:install>
# \ <section:merge>
MERGE  = Makefile README.md apt.txt .gitignore .vscode $(S)
MERGE += $(MODULE).py test_$(MODULE).py requirements.pip
MERGE += static templates
.PHONY: main
main:
	# git push -v
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
