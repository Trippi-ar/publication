Feature('Login');

Scenario('Home ok', ({ I }) => {
  I.amOnPage('https://frontend-4713090974.us-east1.run.app/home');
  I.see('Adventures');
  I.waitForText('test_available', 10);
});
