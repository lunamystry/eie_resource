'use strict';

/* Controllers */

angular.module('app.controllers', []).
  controller('homeCtrl', ['$scope', function($scope) {

  }])
  .controller('usersCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.users = [
      {name:'John', age:25, gender:'boy'},
      {name:'Jessie', age:30, gender:'girl'},
      {name:'Johanna', age:28, gender:'girl'},
      {name:'Joy', age:15, gender:'girl'},
      {name:'Mary', age:28, gender:'girl'},
      {name:'Peter', age:95, gender:'boy'},
      {name:'Sebastian', age:50, gender:'boy'},
      {name:'Erika', age:27, gender:'girl'},
      {name:'Patrick', age:40, gender:'boy'},
      {name:'Samantha', age:60, gender:'girl'}
    ];

    $http({method: 'GET', url: '/users'}).success(function(data) {
      $scope.users = data; // response data
    });

    $scope.oneAtATime = true;

    $scope.groups = [
      {
        title: "Dynamic Group Header - 1",
        content: "Dynamic Group Body - 1"
      },
      {
        title: "Dynamic Group Header - 2",
        content: "Dynamic Group Body - 2"
      }
    ];

    $scope.items = ['Item 1', 'Item 2', 'Item 3'];

    $scope.addItem = function() {
      var newItemNo = $scope.items.length + 1;
      $scope.items.push('Item ' + newItemNo);
    };

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
