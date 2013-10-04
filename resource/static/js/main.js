// Filename: main.js

// Require.js allows us to configure shortcut alias
// There usage will become more apparent further along in the tutorial.
require.config({
  paths: {
    jquery: 'lib/jquery',
    underscore: 'lib/underscore',
    mustache: 'lib/mustache',
    backbone: 'lib/backbone',
    jquery_cookie: 'lib/jquery.cookie',
    prettyPhoto: 'lib/jquery.prettyPhoto',
  },
  shim: {
    'backbone': { deps: ['jquery', 'underscore'], exports: 'Backbone'},
    'jquery_cookie': { deps: ['jquery'], exports: '$.cookie'},
    'prettyPhoto': { deps: ['jquery'], exports: 'prettyPhoto'}
  }
});

require([
  'app',
], function(App){
  App.boot("#resource");
});
