const {
  override,
  overrideDevServer
} = require("customize-cra");

module.exports = {
  // webpack: override(
  //   (config) => {
  //     return config;
  //   }
  // ),
  devServer: overrideDevServer(
    (config) => {
      config.proxy = {
        '/auth': {
          target: 'http://localhost:5000'
        },
        '/api': {
          target: 'http://localhost:5000',
          changeOrigin: true
        }
      };

      return config;
    }
  )
};
