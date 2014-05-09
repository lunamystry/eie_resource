define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
], function($, _, Mustache, Backbone) {

  var Group = Backbone.Model.extend({
    urlRoot: "/groups",
    name: function() { return this.get("name"); },
  });

  return Group;
});
