define([
  'jquery',
  'underscore',
  'backbone',
  'router',
], function($, _, Backbone, Router) {

  boot = function(container) {
    container = $(container);
    var router = new Router({el: container})
    Backbone.history.start();
  }

  return {
    boot: boot
  }
});
