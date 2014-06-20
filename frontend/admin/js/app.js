'use strict';

// Declare app level module which depends on filters, and services
angular.module('resource', [
  'ngRoute',
  'ngResource',
  'ngCookies',
  'ngAnimate',
  'ui.bootstrap',
  'service.version',
  'service.users',
  'service.groups',
  'service.sessions',
  'controller.login',
  'controller.home',
  'controller.users',
  'controller.groups',
  'controller.nav',
  'controller.title',
  'controller.userEdit',
  'filters.version',
  'directives.appVersion',
])
  .config(['$routeProvider', function($routeProvider) {
      $routeProvider.when('/home', {
          templateUrl: 'views/home.html',
          controller: 'homeCtrl'});
      $routeProvider.when('/users', {
          templateUrl: 'views/users.html',
          controller: 'usersCtrl'});
      $routeProvider.when('/groups', {
          templateUrl: 'views/groups.html',
          controller: 'groupsCtrl'});
    $routeProvider.otherwise({redirectTo: '/home'});
  }])
  .run(['$rootScope', '$location', 'SessionUser', function($rootScope, $location, SessionUser) {
    var noAuthRoutes = ['/home'];

    var routeClean = function (route) {
      return _.find(noAuthRoutes, function (noAuthRoute) {
        return route.startsWith(noAuthRoute);
      });
    };

    SessionUser.restore_session();
    $rootScope.$on('$routeChangeStart', function (event, next, current) {
      if (!routeClean($location.url()) && !SessionUser.isLoggedIn) {
        $location.path("/home");
      }
    });
  }]);
