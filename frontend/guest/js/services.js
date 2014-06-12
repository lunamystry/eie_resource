'use strict';

/* Services */

angular.module('app.services', [])
  .factory('Session', ['$resource', function($resource) {
    return $resource('/sessions/:_id', {_id: '@id'})
  }])
  .factory('SessionUser', ['$log', 'Session', function($log, Session) {
      var sessionUser = {
          isLoggedIn: false,
          session: {},
          homePage: "/profile",
          errors: {},
          sign_in: function(username, password, successFn, errorFn) {
              this.session = new Session({"username": username, "password": password});
              this.session.$save(function(value, headers) {
                  sessionUser.isLoggedIn = true;
                  if ("function" == typeof successFn) {
                      successFn(value, headers);
                  }
                  $log.info("logged in: " + username);
              }, function(response) {
                  sessionUser.session = {};
                  sessionUser.isLoggedIn = false;
                  sessionUser.errors = response.data;
                  if ("function" == typeof errorFn) {
                      errorFn(response);
                  }
                  $log.error("could not login: " + username);
              });
      },
      sign_out: function() {
          if (typeof(sessionUser.session._id) != "undefined") {
              sessionUser.session.delete();
              sessionUser.session = {};
              sessionUser.isLoggedIn = false;
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
