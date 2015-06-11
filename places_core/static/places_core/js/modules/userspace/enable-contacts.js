//
// enable-contacts.js
// ==================

// The script checks whether the user has logged in through Google
// and unlocks the abbility to invite freind from Gmail mailbox

require(['jquery', 'js/modules/userspace/google-contacts'],

function ($, ContactListView) {

  "use strict";

  // A query to the server about user contacts

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

  // XML conversion to JS object

  function parseContacts (xml) {

    xml = xml.replace(/gd:email/g, 'email'); // Error in Google Chrome

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

  // We pin in the events and launch the scripts

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
