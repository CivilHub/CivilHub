//
// enable-contacts.js
// ==================

// Skrypt sprawdza, czy użytkownik jest zalogowany przez Google
// i odblokowuje możliwość zapraszania znajomych ze skrzynki Gmail.

require(['jquery', 'js/modules/userspace/google-contacts'],

function ($, ContactListView) {

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
});