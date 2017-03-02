/**
 * Created by LzxHahaha on 2016/5/31.
 */

var path = require('path');
var webpack = require('webpack');

module.exports = {
  entry: [
    'babel-polyfill',
    'whatwg-fetch',
    './index.js'
  ],
  output: {
    path: path.join(__dirname, '/build'),
    filename: 'bundle.js'
  },
  resolve: {
    extensions: ['', '.js', '.jsx', '.css']
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': '"development"'
    })
  ],
  module: {
    loaders: [{
      test: /\.js|jsx$/,
      loaders: ['babel'],
      exclude: /node_modules/,
      loader: "babel",
      query: {
        babelrc: false,
        presets: ['es2015', 'react', 'stage-3'],
        plugins: [
          "transform-class-properties",
          "transform-object-rest-spread"
        ]
      }
    }, {
      test: /\.css|\.scss$/,
      loaders: [
        'style-loader',
        'css-loader?modules&importLoaders=1&localIdentName=[name]__[local]--[hash:base64:5]'
      ]
    }, {
      test: /\.json$/,
      loader: 'json'
    }, {
      test: /\.(png|jpe?g)$/,
      loaders: [
        'url-loader'
      ]
    }]
  },
  devServer: {
    historyApiFallback: true
  }
};