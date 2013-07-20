// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  'state',
  'views/menu',
  'views/index',
  'views/login',
  'views/users_index',
  'jquery_cookie'
], function($, _, Backbone, AppState, MenuView, IndexView, LoginView, UsersView){

  function authorized() {
    if (typeof $.cookie("user_id") != 'undefined') {
      if (typeof $.cookie($.cookie("user_id")) != 'undefined') {
        return true;
      }
    }
    else {
      // TODO: Set error message first
      location.hash = "#login";
      return;
    }
    return;
  };

  var Router = Backbone.Router.extend({
    initialize: function(options) {
      this.el = options.el
      AppState.restoreSession();
      var menu = new MenuView();
      $("#menu").html(menu.render().el);
      this.bind("all", function() {
        menu.render();
      });
    },
    routes: {
      "": "index",
      "index": "index",
      "login": "login",
      "logout": "logout",
      "users": "users",
      "about": "about"
    },
    login: function() {
      document.title = "Sign in - Resource";
      var view = new LoginView();
      this.el.empty();
      this.el.append(view.render().el);
    },
    logout: function() {
      document.title = "Logout - Resource";
      var session = new Ehlane.Session();
      location.hash = "#index";
    },
    index: function() {
      var view = new IndexView();
      this.el.empty();
      this.el.append(view.render().el);
    },
    users: function() {
      document.title = "Users - Resource";
      $("#title").html("Users");
      var view = new UsersView();
      this.el.empty();
      this.el.append(view.render().el);
    },
    about: function() {
      document.title = "About - Resource";
      $("#title").html("About");
      this.el.empty();
      this.el.html("Information about the impact will go here");
    }
  });

  return  Router;
});
