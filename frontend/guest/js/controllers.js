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
  .controller('loginCtrl', ['$scope', '$location', 'SessionUser', function($scope, $location, SessionUser) {
    $scope.sign_in = function() {
        SessionUser.sign_out(); // one user at a time, per client
        if ($scope.login_form.$valid) {
            if(SessionUser.sign_in($scope.username, $scope.password)) {
                $location.path(SessionUser.nextPage);
            } else {
                $scope.has_error = true;
                $scope.login_form.error_message = "could not log you in, you can try again if you want"; 
            }
        }
    }

    $scope.signed_in_user = function() {
      return SessionUser.data.username;
    }
  }])
  .controller('navCtrl', ['$scope','$location', 'SessionUser', function($scope, $location, SessionUser) {
    $scope.navClass = function (page) {
      var currentRoute = $location.path().substring(1) || 'home';
      return page === currentRoute ? 'active' : '';
    };
    $scope.sign_out = function () {
        SessionUser.sign_out();
    }
    $scope.isLoggedIn = function() {
      return SessionUser.isLoggedIn;
    }
  }])
  .controller('profileCtrl', ['$scope', 'SessionUser', 'Users', function($scope, SessionUser, Users) {
    $scope.change_password = function() {
      if ( Users.authenticate()) {
        console.log("Changed password");
        if ( $scope.password_form.new_password == $scope.password_form.new_password2) {
          Users.change_password($scope.password, $scope.new_password);
        } else {
          $scope.password_form.error_message = "Passwords don't match";
        }
      } else {
          $scope.password_form.error_message = "Password is wrong bud!";
      }
    }
  }])
  .controller('titleCtrl', ['$scope','$location', function($scope, $location) {
    $scope.title = function () {
      var currentRoute = $location.path().substring(1) || 'home';
      return currentRoute;
    };
  }]);
