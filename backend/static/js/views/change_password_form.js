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
      var user = new UserModel({"username": $.cookie("username")});
      var new_password = this.$('#new_password input').val();
      var password2 = this.$('#password2 input').val();
      if (new_password == password2) {
        user.save({
          'username': $.cookie("username"),
          'new_password': new_password,
        },{
          success: function(user, response) {
            result = response.result;
            this.$("#new_password input").val("");
            this.$("#password2 input").val("");
            this.$("#new_password .help-inline").html("");
            this.$("#password2 .help-inline").html("");
            this.$("#new_password").removeClass('error');
            this.$("#password2").removeClass('error');
            console.log(user);
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
      } else{
        this.$("#new_password").addClass('error');
        this.$("#password2").addClass('error');
        this.$("#new_password .help-inline").html("Passwords must match");
        this.$("#password2 .help-inline").html("Passwords must match");
      }
    }
  });

  return PasswordForm;
});
