define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/bookings',
  'views/booking'
], function($, _, Mustache, Backbone, BookingsModel, BookingView) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var BookingsList = Backbone.View.extend({
    render: function() {
      this.collection.each(function(booking) {
        var view = new BookingView({model: booking});
        this.$el.append(view.render().el);
      }, this)
        return this;
    }
  });

  return BookingsList;
});
