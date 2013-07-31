define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
], function($, _, Mustache, Backbone) {

  var Booking = Backbone.Model.extend({
    urlRoot: "/bookings",
    idAttribute: "_id",
    name: function() { return this.get("name") ; },
    booking: function() { return this.get("bookingname"); },
    email: function() { return this.get("email"); }
  });

  return Booking;
});
