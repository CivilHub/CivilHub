//
// moment.js
// =========

define(['moment'], function (moment) {

"use strict";

moment.locale(CivilApp.language);

moment.fn.fromNowOrNow = function (a) {
  if (moment().diff(this) < 0) {
    return gettext('just now');
  }
  return this.fromNow(a);
};

return moment;

});
