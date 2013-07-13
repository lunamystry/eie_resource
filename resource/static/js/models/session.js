define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
], function($, _, Mustache, Backbone) {

  var Session = Backbone.Model.extend({
    urlRoot: "/sessions",
    idAttribute: "_id",
    key: function() { return this.get("name"); },
    username: function() { return "username"; },
    timeout: function() { return "timeout"; },
  });

  return Session;
});
