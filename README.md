Instalacja
----------

Programy do zainstalowania z apta:

	python-dev
	virtualenvwrapper
	postgresql-server-dev-all
	libicu-dev
	libjpeg-dev
	libfreetype6-dev
	build-essential
	git
	gettext
	python-geoip
	libxapian-dev
	python-xapian
	binutils
	libproj-dev
	gdal-bin
	nodejs
	nodejs-legacy
	npm

`python-xapian` można zainstalować z innych źródeł. Trzeba go symlinkować do katalogu virtualenva.
Jeżeli nie chcemy korzystać z buildów, `nodejs`, `nodejs-legacy` oraz `npm` są niepotrzebne. Podobnie z `virtualenv`, jeżeli nie chcemy z niego korzystać.

Wszystkie paczki pythona instalujemy za pomocą polecenia:
	pip install -r requirements
wywołanego w katalogu z projektem.

Build
-----

Multirequire zamienia się w `./manage.py build`. Opcje są podobne, tzn. polecenie wywołane bez argumentów kompresuje wszystkie dostępne pliki `less` i `js`.
Dostępne opcje to:
	-m &lt;nazwa_modułu&gt; Nazwa konkretnego modułu do skompresowania, np. `idea-detail`.
	--css-only	kompresuje tylko pliki `less`

Do przebudowania potrzebujemy dwóch paczek, które instalujemy poleceniami:

	npm install -g less
	npm install -g requirejs