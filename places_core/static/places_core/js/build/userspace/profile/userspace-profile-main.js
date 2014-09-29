//
// Strona profilu użytkownika
//
//  => /templates/userspace/profile.html
//
// -------------------------------------

require.config({
    
    baseUrl: window.STATIC_URL,
    
    urlArgs: "bust=" + (new Date()).getTime(),
    
    waitSeconds: 200,
    
    paths: {
        jquery: 'includes/jquery/jquery',
        bootstrap: 'includes/bootstrap/bootstrap',
        underscore: 'includes/underscore/underscore',
        backbone: 'includes/backbone/backbone',
        tagsinput: 'includes/jquery/jquery.tagsinput',
        bootbox: 'includes/bootstrap/bootbox'
    },
    
    shim: {
        underscore: {
            deps: ['jquery'],
            exports: '_'
        },
        
        backbone: {
            deps: ['underscore'],
            exports: 'Backbone'
        },
        
        bootstrap: {
            deps: ['jquery']
        },
        
        bootbox: {
            deps: ['bootstrap'],
            exports: 'bootbox'
        },
        
        tagsinput: {
            deps: ['jquery']
        },
    }
});

require(['jquery',
         'underscore',
         'js/userspace/google-contacts',
         'js/common',
         'js/userspace/actions/actions'],

function($, _, ContactListView) {

    "use strict";
    
    var contactWindow = null; // Globalne dowiązanie do okna kontaktów.

    // Zapytanie do serwera o kontakty użytkownika.

    function fetchContacts (success) {
        $.ajax({
            url: 'https://www.google.com/m8/feeds/contacts/default/full?max-results=9999',
            dataType: 'jsonp',
            data: window.GOOGLE_DATA,
            success: function (data) {
                success(data);
            }
        });
    }
    
    // Konwersja XML do obiektu JS
    
    function parseContacts (xml) {
        
        xml = xml.replace(/gd:email/g, 'email'); // Błąd w Google Chrome
        
        var oParser = new DOMParser(),
            oDOM = oParser.parseFromString(xml, "text/xml"),
            contacts = [],
            name, address = '';

        if (oDOM.documentElement.nodeName == "parsererror") {
            return [{error: "Error while parsing server response"}];
        }
        
        $(oDOM).find('entry').each(function () {
            name = $(this).find('title').text();
            address = $(this).find('email').attr('address');
            if (name.length <= 1) name = address;
            contacts.push({name: name, address: address});
        });
        
        return contacts;
    }

    // Przypinamy wydarzenia i odpalamy skrypty
    
    $('.contacts-toggle').on('click', function (e) {
        
        e.preventDefault();
        
        if (!_.isNull(contactWindow)) {
            contactWindow.open();
            return false;
        }
        
        fetchContacts(function (data) {
            contactWindow = new ContactListView({
                contacts: parseContacts(data)
            });
            contactWindow.open();
        });
    });

    $(document).trigger('load');
});