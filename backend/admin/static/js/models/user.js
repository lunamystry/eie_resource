define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
], function($, _, Mustache, Backbone) {

  var User = Backbone.Model.extend({
    urlRoot: "/users",
    fullname: function() { return this.get("first_name") + " " + this.get("last_name") ; },
    username: function() { return this.get("username"); },
    gender: function() { return this.get("gender"); },
    address: function() { return this.get("address"); },
    email: function() { return this.get("email"); },
    school: function() { return this.get("school"); },
    cellphone_no: function() { return this.get("cellphone_no"); },
    phone_no: function() { return this.get("phone_no"); },
    role_id: function() { return this.get("role_id"); },
  });

  return User;
});
