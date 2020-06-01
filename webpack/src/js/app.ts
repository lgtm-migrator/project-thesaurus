import * as Sentry from '@sentry/browser';
import {Vue as VueIntegration} from '@sentry/integrations';
import PortalVue from 'portal-vue';
import {TiptapVuetifyPlugin} from 'tiptap-vuetify';
import Vue from 'vue';
import VueAsyncComputed from 'vue-async-computed';
import VueI18n from 'vue-i18n';
import VueRouter from 'vue-router';
import VuetifyToast from 'vuetify-toast-snackbar';
import csVuetify from 'vuetify/es5/locale/cs';
import enVuetify from 'vuetify/es5/locale/en';
import Vuetify, {VBtn, VIcon, VSnackbar} from 'vuetify/lib/index';
import '../scss/index.scss';
import App from './App.vue';
import Axios from './axios';
import csLocal from './locale/cs.json';
import enLocal from './locale/en.json';
import {DjangoPermsPlugin, I18nRoutePlugin} from './plugins';
import {createRouter} from './router';
import {OPTIONS_ACTIONS} from './store/options';
import {PERMS_ACTIONS} from './store/perms';
import createStore from './store/store';
import {notificationBus, pageContext, THEME_COLORS} from './utils';

Vue.use(VueI18n);
Vue.use(Vuetify, {
    components: {
        VSnackbar,
        VBtn,
        VIcon
    }
});
Vue.use(VueRouter);
Vue.use(VueAsyncComputed);
Vue.use(PortalVue);
Vue.use(I18nRoutePlugin);
Vue.use(DjangoPermsPlugin);
Vue.use(VuetifyToast, {
    queueable: true,
    x: 'right',
    y: 'top',
    timeout: 6000
});


declare var __SENTRY_DSN__: string;

if (__SENTRY_DSN__) {
    Sentry.init({
        dsn: __SENTRY_DSN__,
        integrations: [new VueIntegration({Vue, attachProps: true})]
    });
}

export default function createVue(opts: any = {}) {
    Vue.config.productionTip = false;

    const {locale} = pageContext;

    const vuetify = new Vuetify({
        lang: {
            locales: {cs: csVuetify, en: enVuetify},
            current: locale
        },
        theme: {
            themes: {
                light: THEME_COLORS
            }
        },
        icons: {
            values: {
                thesis_assigment: 'mdi-file-pdf',
                thesis_text: 'mdi-file-pdf',
                thesis_poster: 'mdi-image',
                supervisor_review: 'mdi-file-pdf',
                opponent_review: 'mdi-file-pdf',
                thesis_attachment: 'mdi-folder-zip'
            }
        }
    });

    const i18n = new VueI18n({locale, messages: {cs: csLocal, en: enLocal}});

    Vue.use(TiptapVuetifyPlugin, {
        vuetify,
        iconsGroup: 'mdi'
    });

    Axios.defaults.headers['Accept-Language'] = locale;

    let store;
    if ('store' in opts)
        store = opts.store;
    else
        store = createStore();

    let router;
    if ('router' in opts)
        router = opts.router;
    else
        router = createRouter((k) => i18n.t(k), store);


    if (store) {
        store.dispatch(`perms/${PERMS_ACTIONS.LOAD_PERMS}`);
        store.dispatch(`options/${OPTIONS_ACTIONS.LOAD_OPTIONS}`);
    }


    const app = new Vue({
        router,
        vuetify,
        store,
        i18n,
        render: h => h(App),
        ...opts
    });

    notificationBus.$on('flash', (flash) => {
        app.$toast(flash.text, {...flash, color: flash.color});
    });

    pageContext.messages.forEach((m) => {
        notificationBus[m.type](m.text);
    });

    return app;
}