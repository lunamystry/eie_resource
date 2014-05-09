define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/users',
], function($, _, Mustache, Backbone, UsersModel, UserView) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var UsersForm = Backbone.View.extend({
    tagName: "form",
    className: "form",
    template: template('user-form'),
    events: {
      "submit": "submit"
    },
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    submit: function(event) {
      event.preventDefault();
      var user = this.collection.create({
        'first_name': this.$('#first_name input').val(),
        'last_name': this.$('#last_name input').val(),
        'username': this.$('#username input').val(),
        'email': this.$('#email input').val(),
        'gender': this.$('#gender input').val(),
        'address': this.$('#address input').val(),
        'school': this.$('#school input').val(),
        'phone_no': this.$('#phone_no input').val(),
        'cellphone_no': this.$('#cellphone_no input').val(),
        'role_id': this.$('#role_id input').val(),
      },{
        wait: true,
        success: function(model, response) {
          console.log(model);
        },
        error: function(model, response) {
          errors = $.parseJSON(response.responseText);
          for (var field in model.attributes) {
            if (model.attributes.hasOwnProperty(field)) {
              this.$('#' + field + " input").val(model.attributes[field]);
              this.$('#' + field).removeClass('error');
            }
          }
          for (var field in errors) {
            if (errors.hasOwnProperty(field)) {
              this.$('#' + field).addClass('error');
              this.$('#' + field + " .help-inline").html(errors[field].join("<br/>"));
            }
          }
        }
      });
    }
  });

  return UsersForm;
});
