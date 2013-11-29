'use strict';

/* Controllers */

angular.module('app.controllers', []).
  controller('homeCtrl', ['$scope', function($scope) {

  }])
  .controller('usersCtrl', ['$scope', '$http', function($scope, $http) {
    $http({method: 'GET', url: '/users'}).success(function(data) {
      $scope.users = data;
    });

    var user = $scope.user = {'last_name':"",
                              "first_name": "",
                              "student_number":"",
                              "yos":3}; // for the form
    $scope.updateUsername = function() {
      if (typeof user.last_name !== 'undefined' && typeof user.first_name !== 'undefined'){
        $scope.user.username = user.last_name.toLowerCase()+user.first_name.toLowerCase().charAt(0);
      } else {
        $scope.user.username = "";
      }

    }
    var studentSuffix = "@students.ug.eie.wits.ac.za";
    var staffSuffix = "@wits.ac.za"
    var emailSuffixes = {1: studentSuffix,
                         2: studentSuffix,
                         3: studentSuffix,
                         4: studentSuffix,
                         5: studentSuffix,
                         6: staffSuffix,
                         7: staffSuffix}
    $scope.updateEmail = function() {
      if(user.yos < 6) {
        $scope.user.email = user.student_number.toLowerCase()+emailSuffixes[user.yos];
      } else {
        $scope.user.email = user.first_name.toLowerCase()+"."+user.last_name.toLowerCase()+staffSuffix;
      }
    }
    user.login_shell = "/bin/bash";
    user.home_directory = "/home/ug/";
    $scope.saveUser = function  () {
      $http.post('/users', user)
        .success(function (user) {
          $scope.users.push(user);
        });
    };
    $scope.deleteUser = function(username) {
      $http({method: 'DELETE', url: '/users/'+ username})
        .success(function(data) {
          for ( var key in $scope.users) {
            if ($scope.users.hasOwnProperty(key)){
              $scope.users.splice(key + 1, 1);
            }
          }
        });
    }

    $scope.userViewCtrl = function($scope) {
      $scope.showEditForm = function() {
        $scope.editing = true;
      }
      $scope.showView = function() {
        $scope.editing = false;
      }
      $scope.editing = false;
    }
  }])
  .controller('userEditCtrl', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
    var username = $routeParams.username;
    $http({method: 'GET', url: '/users/' + username})
      .success(function(data) {
        $scope.users = data;
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
