define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/groups',
  'views/group'
], function($, _, Mustache, Backbone, GroupsModel, GroupView) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var GroupsList = Backbone.View.extend({
    render: function() {
      this.collection.each(function(group) {
        var view = new GroupView({model: group});
        this.$el.append(view.render().el);
      }, this)
        return this;
    }
  });

  return GroupsList;
});
