define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/images',
  'views/image',
  'bootstrap',
  'prettyPhoto'
], function($, _, Mustache, Backbone, ImagesModel, ImageView) {

  var template = function(name) {
    return Mustache.compile($('#'+name+'-template').html());
  };

  var Gallery = Backbone.View.extend({
    className: "gallery row-fluid columned_section",
    template: template('gallery'),
    initialize: function() {
      this.images = new ImagesModel();
      this.images.on('all', this.render, this);
      this.images.fetch();
    },
    render: function() {
      this.$el.empty();
      this.images.each(function(image) {
        var view = new ImageView({model: image});
        this.$el.append(view.render().el);
      }, this);
      $("a[rel^='prettyPhoto']").prettyPhoto({
        allow_resize: true,
        default_width: 500,
        default_height: 344,
      });
      return this;
    },
    count: function() { return this.images.length; },
  });

  return Gallery;

});
