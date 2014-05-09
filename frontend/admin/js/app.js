'use strict';

// Declare app level module which depends on filters, and services
angular.module('resource', [
  'ngRoute',
  'ngResource',
  'ngAnimate',
  'ui.bootstrap',
  'service.version',
  'service.users',
  'controller.home',
  'controller.users',
  'controller.nav',
  'controller.title',
  'controller.userEdit',
  'filters.version',
  'directives.appVersion',
]).
  config(['$routeProvider', function($routeProvider) {
      $routeProvider.when('/home', {
          templateUrl: 'views/home.html',
          controller: 'homeCtrl'});
      $routeProvider.when('/users', {
          templateUrl: 'views/users.html',
          controller: 'usersCtrl'});
      $routeProvider.when('/users/:username', {
          templateUrl: 'views/user_edit.html',
          controller: 'userEditCtrl'});
    $routeProvider.otherwise({redirectTo: '/home'});
  }]);
