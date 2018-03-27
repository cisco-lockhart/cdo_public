/* globals bindings, angular */
'use strict';

var app = angular.module('app', []);

app.controller('MainController', ['$scope', function($scope) {
  $scope.bindings = bindings;
}]);