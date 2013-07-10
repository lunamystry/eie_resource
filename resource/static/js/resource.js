(function() {
  Resource.Router = Backbone.Router.extend({
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
      var view = new Resource.Login();
      this.el.empty();
      this.el.append(view.render().el);
    },
    logout: function() {
      var session = new Resource.Session();
      location.hash = "#index";
    },
    index: function() {
      var view = new Resource.Index();
      this.el.empty();
      this.el.append(view.render().el);
    },
    users: function() {
      var view = new Resource.Users.Index();
      this.el.empty();
      this.el.append(view.render().el);
    },
    groups: function() {
      var view = new Resource.Groups.Index();
      this.el.empty();
      this.el.append(view.render().el);
    },
  });

  Resource.boot = function(container) {
    container = $(container);
    var router = new Resource.Router({el: container})
    Backbone.history.start();
  }
})()
