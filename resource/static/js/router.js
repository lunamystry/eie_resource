// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  'views/index',
  'views/login',
  'views/users_index',
  'jquery_cookie'
], function($, _, Backbone, IndexView, LoginView, UsersView){
  var Router = Backbone.Router.extend({
    initialize: function(options) {
      this.el = options.el
    },
    routes: {
      "": "index",
      "login": "login",
      "logout": "logout",
      "users": "users",
      "about": "about"
    },
    login: function() {
      document.title = "Sign in - eHlane";
      var view = new LoginView();
      this.el.empty();
      this.el.append(view.render().el);
    },
    logout: function() {
      document.title = "Logout - eHlane";
      var session = new Ehlane.Session();
      location.hash = "#index";
    },
    index: function() {
      var view = new IndexView();
      this.el.empty();
      this.el.append(view.render().el);
    },
    users: function() {
      document.title = "Users - eHlane";
      $("#title").html("Users");
      var view = new UsersView();
      this.el.empty();
      this.el.append(view.render().el);
    },
    about: function() {
      document.title = "About - eHlane";
      $("#title").html("About us");
      this.el.empty();
      this.el.html("Information about the impact will go here");
    }
  });

  return  Router;
});
