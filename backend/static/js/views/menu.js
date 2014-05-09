define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'views/login_form',
  'jquery_cookie'
], function($, _, Mustache, Backbone, LoginForm) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var Profile = Backbone.View.extend({
    tagName: "li",
    template: template('nav-profile'),
    initialize: function(options) {
      this.username = options.username;
    },
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    link_href: function() {
      if (typeof this.username == 'undefined') {
        return "login";
      } else {
        return "logout";
      }
    },
    link_name: function() {
      if (typeof this.username == 'undefined') {
        return "sign in";
      } else {
        return "sign out";
      }
    }
  });

  var Menu = Backbone.View.extend({
    tagName: "ul",
    className: "nav-menu pull-right",
    template: template('menu'),
    events: {
      'all': 'render'
    },
    render: function() {
      this.$el.html(this.template(this));
      var profileView = new Profile({"username": $.cookie("username")});
      this.$el.append(profileView.render().el);
      return this;
    },
  });

  return Menu;
});
