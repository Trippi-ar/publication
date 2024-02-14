Feature('Login');

Scenario('Home ok', ({ I }) => {
  I.amOnPage('https://frontend-3bsgyuggyq-ue.a.run.app/home');
  I.see('Adventures');
  I.waitForText('test_available', 10);
});
