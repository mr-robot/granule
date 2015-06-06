'use strict';

/* App Module */
var granuleApp = angular.module('granuleApp', [  'ngRoute', 'angularBasicAuth', 'granuleControllers', 'granuleServices']);

granuleApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/login', {
        templateUrl: 'partials/login.html',
        controller: 'LoginCtrl'
      }).
      when('/activity', {
        templateUrl: 'partials/activity-list.html',
        controller: 'ActivityListCtrl'
      }).
      when('/activity/:activityId', {
        templateUrl: 'partials/activity-detail.html',
        controller: 'ActivityDetailCtrl'
      }).
      otherwise({
        redirectTo: '/login'
      });
  }]);