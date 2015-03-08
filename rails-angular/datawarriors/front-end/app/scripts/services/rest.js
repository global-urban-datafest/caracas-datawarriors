'use strict';

var restServices = angular.module('restServices', ['ngResource']);

restServices.factory('Tweets', [
  '$http',
  'API_PREFIX',
  function($http, API_PREFIX){
    return {
      all: function(gov, category) {
        return $http.get(API_PREFIX + '/tweets.json', {params: {category: category, gov: gov}});
      },
      sentiment: function(gov, category) {
        return $http.get(API_PREFIX + '/tweets/sentiment.json', {params: {category: category, gov: gov}});
      }
    };
}]);

restServices.factory('Categories', [
  '$http',
  'API_PREFIX',
  function($http, API_PREFIX){
    return {
      all: function() {
        return $http.get(API_PREFIX + '/categories.json');
      }
    };
}]);
