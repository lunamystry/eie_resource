'use strict';

var service = angular.module('service.session', []);

service.factory('Session', ['$resource', function($resource) {
    return $resource('/sessions/:_id', {_id: '@id'})
}])
service.factory('SessionUser', [
        '$log', 
        '$http', 
        '$cookieStore', 
        'Session', 
        function($log, $http, $cookieStore, Session) {
            var sessionUser = {
                isLoggedIn: false,
                session: {},
                homePage: "/profile",
                errors: {},
                // TODO: this does not work, fix it
                change_password: function(password, new_password) {
                  $http.put('/passwords/' + sessionUser.session.username,
                            {"password": password, "new_password": new_password}).success(
                              // inform the user
                            ).error(
                              // inform the user
                            );
                },
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
                        if (sessionUser.session.group == 'IT') {
                            sessionUser.homePage = "/admin";
                        }
                        sessionUser.isLoggedIn = true;
                        if ("function" == typeof successFn) {
                            successFn(value, headers);
                        }
                        $cookieStore.put('session_id', sessionUser.session._id);
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
                        sessionUser.session.$remove(sessionUser.session);
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
