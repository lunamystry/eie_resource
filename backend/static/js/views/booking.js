define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
], function($, _, Mustache, Backbone) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var Booking = Backbone.View.extend({
    tagName: "span",
    events: {
      "click .btn-delete": "delete",
      "click .btn-view": "view"
    },
    template: template('booking'),
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    _id: function() { return this.model.id; },
    fullname: function() { return this.model.fullname(); },
    username: function() { return this.model.username(); },
    gender: function() { return this.model.gender(); },
    address: function() { return this.model.address(); },
    email: function() { return this.model.email(); },
    school: function() { return this.model.school(); },
    phone_no: function() { return this.model.phone_no(); },
    cellphone_no: function() { return this.model.cellphone_no(); },
    role_id: function() { return this.model.role_id(); },
    delete: function() {
      this.model.destroy({wait: true});
    },
    view: function() {
      location.hash = "#home/" + this.model.id;
    }
  });

  return Booking;
});
