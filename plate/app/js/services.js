'use strict';

/* Services */

var granuleServices = angular.module('granuleServices', ['ngResource']);

granuleServices.factory('Activity', ['$resource',
  function($resource){
    return $resource('/api/2015-05-30/activity/:activityId', {activityId:'@id'});
  }]);

granuleServices.factory('Item', ['$resource',
  function($resource){
    return $resource('/api/2015-05-30/item/:item', {activityId:'@id'});
  }]);