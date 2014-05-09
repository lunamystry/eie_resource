define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/booking'
], function($, _, Mustache, Backbone, Booking) {

  var Bookings = Backbone.Collection.extend({
    url: "/bookings",
    model: Booking,
    parse: function(response){
      return response.result;
    }
  });

  return Bookings;
});
