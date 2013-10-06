define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/group'
], function($, _, Mustache, Backbone, Group) {

  var Groups = Backbone.Collection.extend({
    url: "/groups",
    model: Group,
    parse: function(response){
      return response.result;
    }
  });

  return Groups;
});
