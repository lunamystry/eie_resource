(function() {
  Ehlane.Router = Backbone.Router.extend({
    initialize: function(options) {
      this.el = options.el
    },
    routes: {
      "": "index",
      "login": "login",
      "logout": "logout",
      "users": "users",
      "groups": "groups",
    },
    login: function() {
      var view = new Ehlane.Login();
      this.el.empty();
      this.el.append(view.render().el);
    },
    logout: function() {
      var session = new Ehlane.Session();
      location.hash = "#index";
    },
    index: function() {
      var view = new Ehlane.Index();
      this.el.empty();
      this.el.append(view.render().el);
    },
    users: function() {
      var view = new Ehlane.Users.Index();
      this.el.empty();
      this.el.append(view.render().el);
    },
    groups: function() {
      var view = new Ehlane.Groups.Index();
      this.el.empty();
      this.el.append(view.render().el);
    },
  });

  Ehlane.boot = function(container) {
    container = $(container);
    var router = new Ehlane.Router({el: container})
    Backbone.history.start();
  }
})()
