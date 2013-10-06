define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
], function($, _, Mustache, Backbone) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var Group = Backbone.View.extend({
    tagName: "span",
    events: {
      "click .btn-delete": "delete",
      "click .btn-view": "view"
    },
    template: template('group'),
    render: function() {
      this.$el.html(this.template(this));
      return this;
    },
    _id: function() { return this.model.id; },
    name: function() { return this.model.name(); },
    delete: function() {
      this.model.destroy({wait: true});
    },
    view: function() {
      location.hash = "#home/" + this.model.id;
    }
  });

  return Group;
});
