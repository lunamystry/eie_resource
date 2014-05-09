define([
  'jquery',
  'underscore',
  'mustache',
  'backbone',
  'models/image',
  'jquery_cookie'
], function($, _, Mustache, Backbone, ImageModel) {

  var Images = Backbone.Collection.extend({
    url: function() { return "/class_photos"},
    sync: function(method, model, options) {
      keyHeader = {"key": $.cookie($.cookie("user_id"))};
      $.ajaxSetup({headers: keyHeader});
      Backbone.sync(method, model, options);
    },
    model: ImageModel,
    parse: function(response){
      return response.result;
    }
  });

  return Images;
});
