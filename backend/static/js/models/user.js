define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
], function($, _, Mustache, Backbone) {

  var User = Backbone.Model.extend({
    urlRoot: "/users",
    idAttribute: "username",
    name: function() { return this.get("name") ; },
    username: function() { return this.get("username"); },
    email: function() { return this.get("email"); }
  });

  return User;
});
