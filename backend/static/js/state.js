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
    $.cookie("username", attributes.username);
    $.cookie(attributes.username, attributes.key);
  };

  var restoreSession = function() {
    if (typeof $.cookie("username") != 'undefined') {
      var session = new SessionModel();
      session.fetch({
        "key": $.cookie($.cookie("username"))
      },{
        success: function(session, response) {
          console.log("Restore a session");
          result = response.result;
          $.cookie("username", result.user_id);
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
    if (typeof $.cookie("username") != 'undefined') {
      $.removeCookie($.cookie($.cookie("username")));
      $.removeCookie("username");
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
