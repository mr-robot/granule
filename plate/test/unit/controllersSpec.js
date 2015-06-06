'use strict';

/* jasmine specs for controllers go here */

describe('controllers', function() {

  it("should do something", function() {

  });

});

describe('ActivityListCtrl', function(){
    var scope, ctrl, $httpBackend;

  beforeEach(module('granuleApp'));

  beforeEach(inject(function(_$httpBackend_, $rootScope, $controller) {
    $httpBackend = _$httpBackend_;
    $httpBackend.expectGET('phones/activities.json').
        respond([{name: 'Nexus S'}, {name: 'Motorola DROID'}]);

    scope = $rootScope.$new();
    ctrl = $controller('ActivityListCtrl', {$scope: scope});
  }));

    it('should create "phones" model with 2 phones fetched from xhr', function() {
      expect(scope.activities).toBeUndefined();
      $httpBackend.flush();

      expect(scope.activities).toEqual([{name: 'Nexus S'},
                                   {name: 'Motorola DROID'}]);
    });




    it('should set the default value of orderProp model', function() {
      expect(scope.orderProp).toBe('age');
    });

});
