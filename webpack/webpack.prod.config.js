const config = require('./webpack.base.config.js');
const webpack = require('webpack');

config.plugins.push(
    new webpack.DefinePlugin({
        '__SENTRY_DSN__': '\'' + process.env.SENTRY_DSN + '\'',
    }),
);

module.exports = config;
