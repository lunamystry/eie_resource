define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'views/login_form'
], function($, _, Mustache, Backbone, LoginForm) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var Login = Backbone.View.extend({
    className: "row-fluid",
    template: template('login'),
    render: function() {
      this.$el.html(this.template(this));
      var loginForm = new LoginForm();
      this.$(".login_form").append(loginForm.render().$el);
      return this;
    },
  });

  return Login;
});
