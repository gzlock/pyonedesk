const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const path = require('path')

const outputDir = path.join(__dirname, '..', 'pyonedesk', 'server', 'res')

console.log({ outputDir })

module.exports = {
  runtimeCompiler: true,
  outputDir,
  assetsDir: 'resources',
  pages: {
    index: {
      entry: 'src/pages/index/main.js',
      title: 'PyOneDesk',
      minify: {
        removeComments: false, // 移除HTML中的注释
        collapseWhitespace: true, // 删除空白符与换行符
        minifyCSS: true,// 压缩内联css
      },
      template: 'public/index.html',
    },
    admin: {
      entry: 'src/pages/admin/main.js',
      filename: 'admin.html',
      title: 'PyOneDesk管理后台',
      template: 'public/admin.html',
    },
    admin_login: {
      entry: 'src/pages/admin_login/main.js',
      filename: 'admin_login.html',
      title: '登录PyOneDesk管理后台',
      template: 'public/admin.html',
    },
    admin_get_code: {
      entry: 'src/pages/admin_get_code/main.js',
      filename: 'admin_get_code.html',
      title: '从微软网站接收Code页面',
      template: 'public/admin_get_code.html',
    },
  },
  productionSourceMap: false,
  devServer: {
    proxy: 'http://localhost:23333/',
  },
  css: {
    loaderOptions: {
      sass: {
        test: /\.scss$/,
        use: [
          process.env.NODE_ENV !== 'production'
            ? 'style-loader'
            : MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader',
        ],
      },
    },
  },
}