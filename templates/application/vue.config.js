const FaviconsWebpackPlugin = require("favicons-webpack-plugin");


module.exports = {
    filenameHashing: false,
    assetsDir: "static",
    publicPath: "/",
    runtimeCompiler: true,
    configureWebpack: {
        plugins: [new FaviconsWebpackPlugin({  // After you change it, copy generated <head> to website index...
          logo: './src/img/favicon.svg',
          inject: true,
          cache: true,
          publicPath: '/static/img',
          outputPath: '../../../static/img',
          prefix: '/static/img',
        })],
    },
};
