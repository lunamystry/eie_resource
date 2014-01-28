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
  .controller('loginCtrl', ['$scope', 'Sessions', function($scope, Sessions) {
    Sessions.query(function(response) {
      $scope.sessions = response;
    });

    $scope.login = function () {
      console.log($scope.username + " " + $scope.password);
    }
  }])
  .controller('navCtrl', ['$scope','$location', function($scope, $location) {
    $scope.navClass = function (page) {
      var currentRoute = $location.path().substring(1) || 'home';
      return page === currentRoute ? 'active' : '';
    };
  }])
  .controller('titleCtrl', ['$scope','$location', function($scope, $location) {
    $scope.title = function () {
      var currentRoute = $location.path().substring(1) || 'home';
      return currentRoute;
    };
  }]);
