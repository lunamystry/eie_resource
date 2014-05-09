// Filename: state.js
define([
  'jquery',
  'underscore',
  'backbone',
  'models/session',
  'jquery_cookie'
], function($, _, Backbone, SessionModel){

  window.AppState = {};

  var newSession = function(attributes) {
    window.AppState.session = new SessionModel(attributes);
    $.cookie("user_id", attributes.user_id);
    $.cookie(attributes.user_id, attributes.key);

  };

  var restoreSession = function() {
    if (typeof $.cookie("user_id") != 'undefined') {
      var session = new SessionModel();
      session.fetch({
        "key": $.cookie($.cookie("user_id"))
      },{
        success: function(session, response) {
          console.log("Restore a session");
          result = response.result;
          $.cookie("user_id", result.user_id);
          $.cookie(result.user_id, result.key);
          newSession(response.result);
        },
        error: function(model, response) {
          window.AppState.session = new SessionModel();
        }
      });
    }
  };

  function endSession() {
    if (typeof $.cookie("user_id") != 'undefined') {
      $.removeCookie($.cookie($.cookie("user_id")));
      $.removeCookie("user_id");
      if (typeof window.AppState.sessoin != 'undefined') {
        window.AppState.session.destroy();
      }
      delete window.AppState.session;
    }
  };

  return {
    restoreSession: restoreSession,
    newSession: newSession,
    endSession: endSession
  };
});
