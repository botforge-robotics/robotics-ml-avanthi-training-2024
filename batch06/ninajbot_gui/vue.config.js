const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  pluginOptions: {
    vuetify: {
      // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
    }
  }
})
// const fs = require('fs')
// module.exports = {
//   devServer: {
//     host: 'dev.local',
//     port: 8080,
//     https: {
//       key: fs.readFileSync('./certs/dev.local+4-key.pem'),
//       cert: fs.readFileSync('./certs/dev.local+4.pem'),
//       //ca: fs.readFileSync('./certs/my-ca.crt')
//     },

//   }
// }