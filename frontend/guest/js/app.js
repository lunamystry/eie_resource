'use strict';

// Declare app level module which depends on filters, and services
angular.module('resource', [
  'ngRoute',
  'ngResource',
  'ngAnimate',
  'ui.bootstrap',
  'app.filters',
  'app.services',
  'app.directives',
  'app.controllers'
]).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/home', {templateUrl: 'views/home.html', controller: 'homeCtrl'});
    $routeProvider.when('/bookings', {templateUrl: 'views/bookings.html', controller: 'bookingsCtrl'});
    $routeProvider.when('/class_photos', {templateUrl: 'views/class_photos.html', controller: 'classPhotosCtrl'});
    $routeProvider.when('/about', {templateUrl: 'views/about.html', controller: 'aboutCtrl'});
    $routeProvider.when('/profile', {templateUrl: 'views/profile.html', controller: 'profileCtrl'});
    $routeProvider.when('/login', {templateUrl: 'views/login.html', controller: 'loginCtrl'});
    $routeProvider.otherwise({redirectTo: '/home'});
  }]).
  run(['$rootScope', '$location', 'SessionUser', function($rootScope, $location, SessionUser) {
    var noAuthRoutes = ['/login', '/about', '/home', '/class_photos'];

    var routeClean = function (route) {
      return _.find(noAuthRoutes, function (noAuthRoute) {
        return route.startsWith(noAuthRoute);
      });
    };

    $rootScope.$on('$routeChangeStart', function (event, next, current) {
      if (!routeClean($location.url()) && !SessionUser.isLoggedIn) {
        $location.path("/login");
      }
    });
  }]);
