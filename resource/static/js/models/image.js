define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
], function($, _, Mustache, Backbone) {

  var Image = Backbone.Model.extend({
    urlRoot: "/class_photos",
    idAttribute: "name",
    name: function() { return this.get("name");},
    url: function() { return this.get("url");},
  });

  return Image;
});
