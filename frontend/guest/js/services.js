'use strict';

/* Services */

angular.module('app.services', [])
  .factory('Session', ['$resource', function($resource) {
    return $resource('/sessions/:_id', {_id: '@id'})
  }])
  .factory('SessionUser', ['$log', '$http', '$cookieStore', 'Session', function($log, $http, $cookieStore, Session) {
      var sessionUser = {
          isLoggedIn: false,
          session: {},
          homePage: "/profile",
          errors: {},
          restore_session: function() {
              if ('undefined' == typeof $cookieStore.get('session_id')) {
                  sessionUser.sign_out();
                  return;
              }
              $http.get('/sessions/'+$cookieStore.get('session_id')).success(
                  function(data, status, headers, config) {
                    sessionUser.session = new Session(data);
                    sessionUser.isLoggedIn = true;
                    $cookieStore.put('session_id', sessionUser.session._id);
                    $log.info("restored session for: " + sessionUser.session.username);
                  })
              .error(function(data, status, headers, config) {
                    sessionUser.sign_out();
                    $log.info("no session could be restored");
              });
          },
          sign_in: function(username, password, successFn, errorFn) {
              this.session = new Session({"username": username, "password": password});
              this.session.$save(function(value, headers) {
                  sessionUser.isLoggedIn = true;
                  $cookieStore.put('session_id', sessionUser.session._id);
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
          sign_out: function(callbackFn) {
              if (typeof(sessionUser.session._id) != "undefined") {
                  sessionUser.session.$delete();
                  sessionUser.session = {};
                  $cookieStore.remove('session_id');
                  sessionUser.isLoggedIn = false;
                  if ("function" == typeof callbackFn) {
                      callbackFn();
                  }
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
