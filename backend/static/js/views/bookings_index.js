define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/bookings',
  'views/bookings_list',
  'views/bookings_form',
], function($, _, Mustache, Backbone, BookingsModel, BookingsList, BookingsForm) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var BookingsIndex = Backbone.View.extend({
    className: "profile row-fluid",
    template: template('bookings-index'),
    initialize: function() {
      this.bookings = new BookingsModel();
      this.bookings.on('all', this.render, this);
      this.bookings.fetch();
    },
    render: function() {
      this.$el.html(this.template(this));
      form = new BookingsForm();
      list = new BookingsList({collection: this.bookings});
      this.$("#bookings-list").append(list.render().el);
      this.$("#bookings-form").append(form.render().el);
      return this;
    },
    name: function() { return this.booking.name(); },
  });

  return BookingsIndex;

});
