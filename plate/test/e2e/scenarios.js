'use strict';

/* http://docs.angularjs.org/guide/dev_guide.e2e-testing */

describe('my app', function() {

  beforeEach(function() {
    browser.get('app/index.html');
  });

});

describe('Granule App', function() {

  describe('Activity list view', function() {

    beforeEach(function() {
      browser.get('app/index.html');
    });

    var query = element(by.model('query'));

    it('should filter the activity list as a user types into the search box', function() {

      var activityList = element.all(by.repeater('activity in activities'));


      expect(activityList.count()).toBe(20);

      query.sendKeys('Power');
      expect(activityList.count()).toBe(6);

      query.clear();
      query.sendKeys('Statistics');
      expect(activityList.count()).toBe(0);
    });

     it('should display the current filter value in the title bar', function() {
      query.clear();
      expect(browser.getTitle()).toMatch(/Granule -\s*$/);

      query.sendKeys('nexus');
      expect(browser.getTitle()).toMatch(/Granule - nexus$/);
    });

 it('should render phone specific links', function() {
      var query = element(by.model('query'));
      query.sendKeys('nexus');
      element.all(by.css('.activities li a')).first().click();
      browser.getLocationAbsUrl().then(function(url) {
        expect(url.split('#')[1]).toBe('/phones/nexus-s');
      });
    });

    it('should be possible to control activity order via the drop down select box', function() {

      var activityNameColumn = element.all(by.repeater('activity in activities').column('activity.name'));
      var query = element(by.model('query'));

      function getNames() {
        return activityNameColumn.map(function(elm) {
          return elm.getText();
        });
      }

      query.sendKeys('Power'); //let's narrow the dataset to make the test assertions shorter

      expect(getNames()).toEqual([ 'Motorola XOOM™ with Wi-Fi', 'MOTOROLA XOOM™', 'MOTOROLA ATRIX™ 4G', 'LG Axis', 'Samsung Galaxy Tab™', 'Samsung Transform™' ]);

      element(by.model('orderProp')).element(by.css('option[value="name"]')).click();

      expect(getNames()).toEqual([ 'LG Axis', 'MOTOROLA ATRIX™ 4G', 'MOTOROLA XOOM™', 'Motorola XOOM™ with Wi-Fi', 'Samsung Galaxy Tab™', 'Samsung Transform™' ] );
    });
  });
});
