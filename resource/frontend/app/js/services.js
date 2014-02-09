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
  .factory('Users', ['$http', 'Session',function($http, Session) {
    var user = {
      authenticate: function() {
        return true;
      },
      change_password: function(oldpw, newpw) {
        // Need this to be synchronous
        $http.put('/password/').success(
          // inform the user
        ).error(
          // inform the user
        );
      }
    }
    return user;
  }])
  .value('version', '0.1');
