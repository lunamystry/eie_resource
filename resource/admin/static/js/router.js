// Filename: admin.router.js
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
      "users": "users",
      "machines": "machines",
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
    machines: function() {
      document.title = "Users - Resource";
      $("#title").html("Users");
      var view = new UsersView();
      this.el.empty();
      this.el.append(view.render().el);
    }
  });

  return  Router;
});
