define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'jquery_cookie'
], function($, _, Mustache, Backbone) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var Image = Backbone.View.extend({
    tagName: "span",
    className: "span5",
    template: template('image'),
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    view: function() {
      location.hash = "#image/" + this.model.name;
    },
    name: function() { return this.model.name();},
    url: function() { return this.model.url();},
  });

  return Image;
});
