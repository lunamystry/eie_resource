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
    $routeProvider.when('/home', {templateUrl: 'partials/home.html', controller: 'homeCtrl'});
    $routeProvider.when('/bookings', {templateUrl: 'partials/bookings.html', controller: 'bookingsCtrl'});
    $routeProvider.when('/class_photos', {templateUrl: 'partials/class_photos.html', controller: 'classPhotosCtrl'});
    $routeProvider.when('/about', {templateUrl: 'partials/about.html', controller: 'aboutCtrl'});
    $routeProvider.when('/login', {templateUrl: 'partials/login.html', controller: 'loginCtrl'});
    $routeProvider.otherwise({redirectTo: '/login'});
  }]).
  run(['$rootScope', '$location', 'Session', function($rootScope, $location, Session) {
    var noAuthRoutes = ['/login', '/about', '/home', '/class_photos'];

    var routeClean = function (route) {
      return _.find(noAuthRoutes, function (noAuthRoute) {
        return route.startsWith(noAuthRoute);
      });
    };

    $rootScope.$on('$routeChangeStart', function (event, next, current) {
      console.log(Session.isLogged);
      if (!routeClean($location.url()) && !Session.isLogged) {
        $location.path("/login");
      }
    });
  }]);
