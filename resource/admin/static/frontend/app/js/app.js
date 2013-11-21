'use strict';

// Declare app level module which depends on filters, and services
angular.module('ehlane', [
  'ngRoute',
  'app.filters',
  'app.services',
  'app.directives',
  'app.controllers',
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/home', {templateUrl: 'partials/home.html', controller: 'homeCtrl'});
  $routeProvider.when('/users', {templateUrl: 'partials/users.html', controller: 'usersCtrl'});
  $routeProvider.when('/bookings', {templateUrl: 'partials/bookings.html', controller: 'bookingsCtrl'});
  $routeProvider.when('/class_photos', {templateUrl: 'partials/class_photos.html', controller: 'classPhotosCtrl'});
  $routeProvider.when('/about', {templateUrl: 'partials/about.html', controller: 'aboutCtrl'});
  $routeProvider.when('/login', {templateUrl: 'partials/login.html', controller: 'loginCtrl'});
  $routeProvider.otherwise({redirectTo: '/home'});
}]);
