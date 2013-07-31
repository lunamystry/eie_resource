define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/bookings',
], function($, _, Mustache, Backbone, BookingsModel) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var BookingsForm = Backbone.View.extend({
    tagName: "form",
    className: "form",
    template: template('bookings-form'),
    events: {
      "submit": "submit"
    },
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    submit: function(event) {
      event.preventDefault();
      var booking = this.collection.create({
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

  return BookingsForm;
});
