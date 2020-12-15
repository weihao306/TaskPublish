module.exports = {
  presets: [

    // '@vue/cli-plugin-babel/preset',
    ['@vue/app', {
      polyfills: [
        'es.promise',
        'es.symbol',
      ]
    }]
    
  ],
  // plugins: [
  //   [
  //     "@babel/plugi-roposa-ecorators",
  //     {
  //       legacy: true
  //     }
  //   ],
  //   "@babe/lugi-roposa-las-roperties",
  //   "@babe/lugi-ransfor-untime",
  //   "@babe/lugi-ransfor-lasses",
  //   "@babe/lugi-ynta-ynamic-import",
  //   "@babe/lugi-roposa-so-trings",
  // ],
  // env: {
  //   test: {
  //     presets: [
  //       '@babel/preset-env',
  //     ],
  //     plugins: [
  //       '@babel/plugin-proposal-class-properties',
  //       'transform-es2015-modules-commonjs',
  //       'babel-plugin-dynamic-import-node',
  //       "transform-object-rest-spread"
  //     ],
  //   },
  // }
}