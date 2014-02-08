'use strict';

/* Services */

angular.module('app.services', []).
  factory('Sessions', ['$resource', function($resource) {
    return $resource('/sessions/:_id', {_id: '@id'})
  }])
  .factory('Session', [function() {
    var sdo = {
      isLogged: false,
      data: {},
      isLoggedIn: function() {
        return IsLogged;
      }
    };
    return sdo;
  }])
  .factory('Users', ['$http', function($http) {
    var user = {
      authenticate: function() {
        return true;
      },
      change_password: function(oldpw, newpw) {
        // Need this to be synchronous
        $http.get('').success(
          // inform the user
        ).error(
          // inform the user
        );
      }
    }
    return user;
  }])
  .value('version', '0.1');
