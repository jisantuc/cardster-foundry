import Ember from 'ember';

export default Ember.Controller.extend({
  session: Ember.inject.service(),

  actions: {
    login() {
      console.log('login');
      this.get('session').authenticate('authenticator:torii', 'github');
    }
  }
});
