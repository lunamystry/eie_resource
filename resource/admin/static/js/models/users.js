define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/user'
], function($, _, Mustache, Backbone, User) {

  var Users = Backbone.Collection.extend({
    url: "/users",
    model: User,
    parse: function(response){
      return response.result;
    }
  });

  return Users;
});
