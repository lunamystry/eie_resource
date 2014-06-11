'use strict';

/* Services */

angular.module('app.services', []).
  factory('Sessions', ['$resource', function($resource) {
    return $resource('/sessions/:_id', {_id: '@id'})
  }])
  .factory('SessionUser', ['Sessions', function(Sessions) {
    var sessionUser = {
      isLoggedIn: false,
      data: {},
      nextPage: "/profile",
      sign_in: function(username, password) {
          Sessions.save({"username": username, "password": password},
              function(response) {
                  this.data = response.result;
                  isLoggedIn = true;
              }, function (response) {
                  isLoggedIn = false;
              });
          // Maybe somehow return the error message aswell?
          return isLoggedIn;
      },
      sign_out: function() {
          if (typeof(this.data.session_id) != "undefined") {
              Sessions.delete(this.data.session_id);
              this.data = {};
              return true;
          }
      }
    };
    return sessionUser;
  }])
  .factory('Users', ['$http', 'SessionUser',function($http, SessionUser) {
    var user = {
      authenticate: function() {
        return true;
      },
      change_password: function(password, new_password) {
        // Need this to be synchronous
        console.log(SessionUser.data.username);
        $http.put('/passwords/' + SessionUser.data.username + '/' + SessionUser.data.key,
                  {"password": password, "new_password": new_password}).success(
                    // inform the user
                  ).error(
                    // inform the user
                  );
      }
    }
    return user;
  }])
  .value('version', '0.1');
