const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const path = require('path')

const outputDir = path.join(__dirname, '..', 'python', 'server', 'res')

console.log({ outputDir })

module.exports = {
  // publicPath: process.env.NODE_ENV === 'production' ? '/' : '/html',
  runtimeCompiler: true,
  outputDir,
  assetsDir: 'resources',
  pages: {
    index: { entry: 'src/pages/index/main.js', title: '首页' },
    admin: {
      entry: 'src/pages/admin/main.js',
      filename: 'admin.html',
      title: 'PyOneDrive管理后台',
    },
    admin_login: {
      entry: 'src/pages/admin_login/main.js',
      filename: 'admin_login.html',
      title: '登录PyOneDrive管理后台',
    },
    admin_get_code: {
      entry: 'src/pages/admin_get_code/main.js',
      filename: 'admin_get_code.html',
      title: '从微软网站接收Code页面',
      template: 'public/admin_get_code.html',
    },
  },
  devServer: {
    /*proxy: {//配置跨域
      '/admin': {
        target: 'http://localhost:23333/admin/',//这里后台的地址模拟的;应该填写你们真实的后台接口
        ws: true,
        changOrigin: true,//允许跨域
        pathRewrite: {
          '^/admin': ''//请求的时候使用这个api就可以
        }
      }
    }*/
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