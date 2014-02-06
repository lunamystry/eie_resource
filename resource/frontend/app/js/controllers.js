'use strict';

/* Controllers */

angular.module('app.controllers', []).
  controller('homeCtrl', ['$scope', function($scope) {

  }])
  .controller('bookingsCtrl', [function() {

  }])
  .controller('classPhotosCtrl', ['$scope', '$http', function($scope, $http) {
    $http.get('class_photos.json').success(function(data) {
      $scope.class_photos = data;
    });
  }])
  .controller('aboutCtrl', [function() {

  }])
  .controller('loginCtrl', ['$scope', '$location', 'Sessions', 'Session', function($scope, $location, Sessions, Session) {
    $scope.user = {}

    $scope.sign_in = function () {
      if ($scope.login_form.$valid) {
        Sessions.save({"username": $scope.username, "password": $scope.password},
                      function(response) {
                        Session.data = response.result;
                        Session.isLogged = true;
                        $location.path("/home");
                      }, function (response) {
                        $scope.has_error = true;
                        $scope.login_form.error_message = response.data["username"];
                      });
      }
    }
    $scope.signed_in_user = function() {
      return Session.data.username;
    }
  }])
  .controller('navCtrl', ['$scope','$location', 'Sessions', 'Session', function($scope, $location, Sessions, Session) {
    $scope.navClass = function (page) {
      var currentRoute = $location.path().substring(1) || 'home';
      return page === currentRoute ? 'active' : '';
    };
    $scope.sign_out = function () {
      Sessions.delete({"_id": Session.data._id}, function(response) {
        Session.data = {};
        Session.isLogged = false;
        $location.path("/login");
      });
    }
    $scope.isLogged = function() {
      return Session.isLogged;
    }
  }])
  .controller('titleCtrl', ['$scope','$location', function($scope, $location) {
    $scope.title = function () {
      var currentRoute = $location.path().substring(1) || 'home';
      return currentRoute;
    };
  }]);
