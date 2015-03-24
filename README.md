CivilHub
----------
CivilHub is a free and open-source platform written in Python & Django for the purpose of collaboration in  local civic communities. 

Our biggest dream is to build a tool that helps us to collaborate and communicate in places we live in. In our opinion, citizens need a platform that will help them transform democracy and civil power onto a next level. 

We believe that together we can create amazing things in our cities.

Our Mission
----------
CivilHub’s mission is to engage all citizens in improving the countries, cities and all places they live in.

Features
----------
1. **Places** - each country, town, district and housing can have their own place that allows people to collaborate.
2. **Ideas** - users can propose what should be improved in our environment, law, and community.
  - Everyone can vote for ideas. Vote Yes or No, 
  - Anyone can check who vote Yes and who No,
  - You can add photos, and use a rich-text editor to create content,
3. **News** - a simple and powerful way to inform users what happend in our community,
4. **Discussions** - a multithreaded forum for places, has categories and tags. 
5. **Polls** - users can create polls for people in Places. All answers and statistics are public
6. **Projects** - one of most the most important part of our platform. I bielieve that Ideas on their own can't change the World. We have created a tool that allows to transform ideas into local civil projects. Users can create and divade tasks, to bring the project to alive.  All of this was made in order to implement our ideas into life.
7. **Map** - all content types can be marked on a map. You can see all the initiatives, discussions, projects and locations in a fully interactive map. Due to limitations in Google Maps (not a good solution for Clustering and displaying more than 100 thousand points on a map). We had to write our own solutions.
  - We used the Open Street Map - Taile are currently downloaded from Mapbox, in the future we will possibly implement our own server with map tails,
  - PostGIS for PostgreSQL database,
  - Our overlay clustering, server-side filtering displays only those points that you currently see on the screen.
8. **Comments** - Disqus was our inspiration, the best comments that exist. You can comment on all of the portal’s content,
User profiles - You can see all user activities and all users in the location you belong to.
  - Login and registration via Facebook, Twitter, LinkedIn and Google+
9. **Messages between users** - a simple system for communication between users, with anti spam security,
10. **Categories** - all content can be categorized, 
11. **Tags** - all content in the portal can be tagged,
12. **Bookmarks** - all types of content can be bookmarked and later on accessed,
13. **Filter and sort** -  all content type,
14. **Search** - the ability to search through all available in the portal content is possible through Xapian & Haystack,
15. **Redis cache** - for each language version we cache most of the content through Redis,
16. **Mail** - we have created a simple and automatic, cyclic system that allows to send emails with information to users about locations they are currently following,
17. **Invite friends** -  from Google+ contacts,
18. **Multilingualism** - both the whole structure of the portal and the database models can be translated. Please help us translate CivilHub to Your language. portal: https://www.transifex.com/projects/p/civilhub/
19. **REST API** - Access to all data stored in https://civilhub.org

About Us
----------
We are a group of young people, living in Warsaw (Poland) who who want to live in a better country and city.

Contact Us
----------
Grzegorz Warzecha - https://www.facebook.com/gwarzecha or grzegorz@civilhub.org


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

Multirequire  `./manage.py build`. Build and compress `less` and `js`.
Options:
	-m &lt;module_name&gt; Module name to compress, np. `idea-detail`.
	--css-only	compress only `less` files

To rebuild you need two packages:

	npm install -g less
	npm install -g requirejs
