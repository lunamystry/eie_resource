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
  'app.controllers',
]).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/home', {templateUrl: 'partials/home.html', controller: 'homeCtrl'});
    $routeProvider.when('/users', {templateUrl: 'partials/users.html', controller: 'usersCtrl'});
    $routeProvider.when('/users/:username', {templateUrl: 'partials/user_edit.html', controller: 'userEditCtrl'});
    $routeProvider.otherwise({redirectTo: '/home'});
  }]);
