define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
], function($, _, Mustache, Backbone) {

  var Group = Backbone.Model.extend({
    urlRoot: "/groups",
    idAttribute: "_id",
    name: function() { return this.get("name"); },
  });

  return Group;
});
