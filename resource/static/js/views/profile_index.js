define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/user',
], function($, _, Mustache, Backbone, UserModel) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var UsersIndex = Backbone.View.extend({
    className: "profile row-fluid",
    template: template('profile'),
    initialize: function() {
      this.user = new UserModel({'username': $.cookie('username')});
      this.user.on('all', this.render, this);
      this.user.fetch();
    },
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    name: function() { return this.user.name(); },
  });

  return UsersIndex;

});
