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
  .controller('loginCtrl', ['$scope', 'Sessions', 'Session', function($scope, Sessions, Session) {
    Sessions.query(function(response) {
      $scope.sessions = response;
    });

    $scope.login = function () {
      Sessions.save({"username": $scope.username, "password": $scope.password}, function(response) {
        Session.data = response.result;
        Session.isLogged = true;
      });
    }
  }])
  .controller('navCtrl', ['$scope','$location', 'Session', function($scope, $location, Session) {
    $scope.navClass = function (page) {
      var currentRoute = $location.path().substring(1) || 'home';
      return page === currentRoute ? 'active' : '';
    };
    $scope.signed_in = function() {
      if (Session.isLogged) {
        return Session.data.username;
      } else {
        return "sign in"
      }
    }
  }])
  .controller('titleCtrl', ['$scope','$location', function($scope, $location) {
    $scope.title = function () {
      var currentRoute = $location.path().substring(1) || 'home';
      return currentRoute;
    };
  }]);
