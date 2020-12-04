import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import {
  colors
} from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        majorColor: colors.amber.darken1,
      }
    }
  }
});