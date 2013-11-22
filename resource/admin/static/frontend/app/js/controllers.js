'use strict';

/* Controllers */

angular.module('app.controllers', []).
  controller('homeCtrl', ['$scope', function($scope) {

  }])
  .controller('usersCtrl', ['$scope', '$http', function($scope, $http) {

    $http({method: 'GET', url: '/users'}).success(function(data) {
      $scope.users = data; // response data
    });

    $scope.selection = 'view';
    $scope.switchToEdit = function(username) {
      $scope.selection = username + '-view';
    }
    $scope.switchToView = function(username) {
      $scope.selection = 'view';
    }

  }])
  .controller('userEditCtrl', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
    var username = $routeParams.username;
    $http({method: 'GET', url: '/users/' + username}).success(function(data) {
      $scope.users = data; // response data
    });
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
  .controller('loginCtrl', [function() {

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
