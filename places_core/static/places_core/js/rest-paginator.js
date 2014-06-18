// Create paginator
// ----------------
// @param options {object} Object containing necessary options:
//   - baseUrl : Base app url to fetch data from.
//   - total   : Total elements count in current set.
//   - perPage : Number of elements to display on one page.
//   - previous: Previous link provided by REST framework.
//   - next    : Next link provided by REST framework.
// @returns {jQuery DOMElement}
var paginator = function (options) {
    
    "use strict";
    
    var defaults = {
        firstPageLabel: '<<',
        lastPageLabel : '>>',
        prevPageLabel : gettext('Previous'),
        nextPageLabel : gettext('Next'),
        className     : 'pagination',
        entryClassName: 'paginator-page',
        activeClass   : 'paginator-active',
        callback      : false,
        showEmpty     : false
    };
    
    options = $.extend(defaults, options);
    
    var pgn = {
        $el: $(document.createElement('div'))
    };

    pgn.$el.addClass(options.className);
    
    // Total pages
    var pages = Math.floor(options.total / options.perPage);
    
    var createLink = function (url, text) {
        var a = $(document.createElement('a')),
            url = url || "#";
        a.text(text).attr('href', url);
        if (url !== "#") {
            a.on('click', function (e) {
                e.preventDefault();
                if (typeof(options.callback) === 'function') {
                    options.callback(url);
                }
            });
        }
        return a;
    };

    var cleanUrl = function () {
        var url = options.baseUrl;
        if (url.indexOf('page') > -1) {
            url = url.slice(0, url.indexOf('page') + 5);
        } else {
            url = url + '&page=';
        }
        return url;
    };
    
    var getCurrentPage = function () {
        var url = options.baseUrl;
        if (url.indexOf('page') > -1) {
            return url.slice(url.indexOf('page') + 5);
        } else {
            return !options.next ? pages : 1;
        }
    };
    
    pgn.$el.append(createLink(cleanUrl() + 1, options.firstPageLabel));
    
    if (options.previous) {
        pgn.$el.append(createLink(options.previous, options.prevPageLabel));
    }
    // Add numeric links to pages in-between.
    for (var i = 1; i <= pages; i++) {
        (function () {
            var l = createLink(cleanUrl() + i, i);
            if (i == getCurrentPage()) { // == is mandatory here.
                l.addClass(options.activeClass);
            }
            pgn.$el.append(l);
        })();
    }
    
    if (options.next) {
        pgn.$el.append(createLink(options.next, options.nextPageLabel));
    }
    
    pgn.$el.append(createLink(cleanUrl() + pages, options.lastPageLabel));
    
    // We don't want paginating one page results - return dummy string.
    if (pages <= 1 && !options.showEmpty) {
        return '';
    }
    // Return DOM element
    return pgn.$el;
};
