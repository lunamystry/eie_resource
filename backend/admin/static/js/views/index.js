define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
], function($, _, Mustache, Backbone) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

   var Index = Backbone.View.extend({
    template: template('index'),
    render: function() {
      this.$el.html(this.template(this));
      return this;
    }
  });

  return Index;
});
