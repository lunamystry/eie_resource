define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/groups',
], function($, _, Mustache, Backbone, GroupsModel, GroupView) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var GroupsForm = Backbone.View.extend({
    tagName: "form",
    className: "form",
    template: template('group-form'),
    events: {
      "submit": "submit"
    },
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    submit: function(event) {
      event.preventDefault();
      var group = this.collection.create({
        'name': this.$('#name input').val(),
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

  return GroupsForm;
});
