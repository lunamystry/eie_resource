'use strict';

/* Services */

angular.module('app.services', []).
  factory('Sessions', ['$resource', function($resource) {
    return $resource('/sessions/:_id', {_id: '@id'})
  }]).
  factory('Session', [function() {
    var sdo = {
      isLogged: false,
      data: {}
    };
    return sdo;
  }]).
  value('version', '0.1');
