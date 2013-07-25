define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'state',
  'models/session',
  'jquery_cookie'
], function($, _, Mustache, Backbone, AppState, SessionModel) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var LoginForm = Backbone.View.extend({
    tagName: "form",
    className: "form",
    template: template('login-form'),
    events: {
      "submit": "submit"
    },
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    submit: function(event) {
      event.preventDefault();
      var session = new SessionModel();
      session.save({
        'username': this.$('#username input').val(),
        'password': this.$('#password input').val(),
      },{
        success: function(session, response) {
          result = response.result;
          AppState.newSession(response.result);
          location.hash = "#profile"
        },
        error: function(model, response) {
          errors = $.parseJSON(response.responseText);
          for (var field in model.attributes) {
            if (model.attributes.hasOwnProperty(field)) {
              this.$('#' + field + " input").val(model.attributes[field]);
              this.$('#' + field + " .help-inline").html("");
              this.$('#' + field).removeClass('error');
            }
          }
          for (var field in errors) {
            if (errors.hasOwnProperty(field)) {
              this.$('#' + field).addClass('error');
              this.$('#' + field + " .help-inline").html(errors[field]);
            }
          }
        }
      });
    }
  });

  return LoginForm;
});