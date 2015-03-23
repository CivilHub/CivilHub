Installation
----------

Apps to install from apta:

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

`python-xapian` you can install from different sources. You must symlink to virtualenv folder.
You do not have to use builds, `nodejs`, `nodejs-legacy`, `npm`, `virtualenv`.

App python packages install:
	pip install -r requirements

Build
-----

Multirequire zamienia się w `./manage.py build`. Opcje są podobne, tzn. polecenie wywołane bez argumentów kompresuje wszystkie dostępne pliki `less` i `js`.
Dostępne opcje to:
	-m &lt;nazwa_modułu&gt; Nazwa konkretnego modułu do skompresowania, np. `idea-detail`.
	--css-only	kompresuje tylko pliki `less`

To rebuild you need two packages:

	npm install -g less
	npm install -g requirejs
