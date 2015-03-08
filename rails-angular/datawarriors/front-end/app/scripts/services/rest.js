'use strict';

var restServices = angular.module('restServices', ['ngResource']);

restServices.factory('Tweets', [
  '$http',
  'API_PREFIX',
  function($http, API_PREFIX){
    return {
      getall: function(gov, category) {
        return $http.post(API_PREFIX + '/tweets.json', {category: category, gov: gov});
      },
      getsentiment: function(gov, category) {
        return $http.post(API_PREFIX + '/tweets.json', {category: category, gov: gov});
      }
      //getone: function(id) {
        //return $http.get(API_PREFIX + '/establishments/'+ id +'.json');
      //},
      //users: function(id){
        //return $http.get(API_PREFIX + '/establishments/' + id + '/users.json');
      //},
      //getall: function() {
        //return $http.get(API_PREFIX + '/establishments.json');
      //},
      //getall_sa: function () {
        //return $http.get(API_PREFIX + '/establishments/all.json');
      //}
    };
}]);
