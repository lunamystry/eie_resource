define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/users',
  'views/users_list',
  'views/users_form'
], function($, _, Mustache, Backbone, UsersModel, UsersList, UsersForm) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var UsersIndex = Backbone.View.extend({
    className: "users row-fluid",
    template: template('users-index'),
    initialize: function() {
      this.users = new UsersModel();
      this.users.on('all', this.render, this);
      this.users.fetch();
    },
    render: function() {
      this.$el.html(this.template(this));
      var usersView = new UsersList({collection: this.users});
      var form = new UsersForm({collection: this.users});
      this.$("#users_list").append(usersView.render().$el);
      this.$("#users_form").append(form.render().$el);
      return this;
    },
    count: function() { return this.users.length; },
  });

  return UsersIndex;

});
