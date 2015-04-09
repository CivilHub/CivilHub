//
// mesages.js
// ==========

// Show all django flash messages as unified
// flash messages from the rest of views.

require(['underscore',
				 'js/modules/ui/ui'],

function (_, ui) {

"use strict";

if (_.isUndefined(CivilApp)) {
	return;
}

_.each(CivilApp.messages, function (m) {
  ui.message.addMessage(m.message, m.level);
});

});
