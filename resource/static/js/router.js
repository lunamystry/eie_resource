// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  'state',
  'views/menu',
  'views/index',
  'views/login',
  'views/profile_index',
  'views/bookings_index',
  'views/class_photos',
  'jquery_cookie'
], function($, _, Backbone, AppState,
     MenuView,
     IndexView,
     LoginView,
     ProfileView,
     BookingsView,
     ClassPhotosView){

  function authorized() {

    if (typeof $.cookie("username") != 'undefined') {
      if (typeof $.cookie($.cookie("username")) != 'undefined') {
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
      "about": "about",
      "bookings": "bookings",
      "profile": "profile",
      "class_photos": "class_photos",
      "login": "login",
      "logout": "logout"
    },
    login: function() {
      document.title = "Sign in - Resource";
      var view = new LoginView();
      this.el.empty();
      this.el.append(view.render().el);
    },
    logout: function() {
      document.title = "Logout - Resource";
      AppState.endSession();
      location.hash = "#login";
    },
    index: function() {
      var view = new IndexView();
      this.el.empty();
      this.el.append(view.render().el);
    },
    about: function() {
      document.title = "About - Resource";
      this.el.empty();
      this.el.html("This has information about the dlab and some useful links");
    },
    profile: function() {
      if(authorized()) {
        document.title = "Profile - Resource";
        var view = new ProfileView();
        this.el.empty();
        this.el.append(view.render().el);
      }

    },
    book: function() {
      document.title = "About - Resource";
      this.el.empty();
      this.el.html("Under construction");
    },
    bookings: function() {
      document.title = "Bookings - Resource";
      var view = new BookingsView();
      this.el.empty();
      this.el.append(view.render().el);
    },
    class_photos: function() {
      document.title = "Class Photos - Resource";
      this.el.empty();
      var view = new ClassPhotosView();
      this.el.append(view.render().el);
    }
  });
  return  Router;
});
