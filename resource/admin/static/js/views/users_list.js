define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/users',
  'views/user'
], function($, _, Mustache, Backbone, UsersModel, UserView) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var UsersList = Backbone.View.extend({
    render: function() {
      this.collection.each(function(user) {
        var view = new UserView({model: user});
        this.$el.append(view.render().el);
      }, this)
        return this;
    }
  });

  return UsersList;
});
