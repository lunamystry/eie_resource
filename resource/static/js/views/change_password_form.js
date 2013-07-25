define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'state',
  'models/user',
  'jquery_cookie'
], function($, _, Mustache, Backbone, AppState, UserModel) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var PasswordForm = Backbone.View.extend({
    tagName: "form",
    className: "form",
    template: template('change-password-form'),
    events: {
      "submit": "submit"
    },
    render: function() {
      this.$el.html(this.template(this));
      this.$('#username input').val($.cookie("username"));
      return this;
    },
    submit: function(event) {
      event.preventDefault();
      var user = new UserModel();
      user.save({
        'username': this.$('#username input').val(),
        'password': this.$('#password input').val(),
      },{
        success: function(user, response) {
          result = response.result;
          location.hash = "#home"
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

  return PasswordForm;
});
