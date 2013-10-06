define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/groups',
  'views/groups_list',
  'views/groups_form'
], function($, _, Mustache, Backbone, GroupsModel, GroupsList, GroupsForm) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var GroupsIndex = Backbone.View.extend({
    className: "groups row-fluid",
    template: template('groups-index'),
    initialize: function() {
      this.groups = new GroupsModel();
      this.groups.on('all', this.render, this);
      this.groups.fetch();
    },
    render: function() {
      this.$el.html(this.template(this));
      var groupsView = new GroupsList({collection: this.groups});
      var form = new GroupsForm({collection: this.groups});
      this.$("#groups_list").append(groupsView.render().$el);
      this.$("#groups_form").append(form.render().$el);
      return this;
    },
    count: function() { return this.groups.length; },
  });

  return GroupsIndex;

});
