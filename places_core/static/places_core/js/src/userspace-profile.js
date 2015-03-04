//
// userspace-profile.js
// ====================
// 
// Profil użytkownika udostępniony do przeglądania przez inne osoby.

require([window.STATIC_URL + "/js/config.js"], function () {
  require(['jquery',
           'underscore',
           'js/modules/userspace/google-contacts',
           'js/modules/userspace/user-follow',
           'js/modules/common',
           'js/modules/userspace/actions/actions'],

  function($, _, ContactListView) {

    "use strict";

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
    
    $(document).ready(function () {
        
      if (GOOGLE_DATA !== undefined && GOOGLE_DATA.access_token) {
          
        var contacts;
        
        $('.contacts-toggle').show().on('click', function (e) {
          e.preventDefault();
          var $modal = $('#google-contacts-modal');
          $modal.one('shown.bs.modal', function () {
            fetchContacts(function (data) {
              $('#contact-list').empty();
              contacts = new ContactListView({
                contacts: parseContacts(data)
              });
            });
          });
          $modal.modal('toggle');
        });
      }
    });

    $(document).trigger('load');
  });
});