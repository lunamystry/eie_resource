'use strict';

/* Services */

angular.module('app.services', []).
  factory('Users', ['$resource', function($resource) {
      return $resource('/users/:username', {username: '@username'})
    }
  ]).
  value('version', 'v0.7.1');
