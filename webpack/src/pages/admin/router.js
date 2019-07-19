import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/home'
import AccountAdd from './views/account-add'
import AccountForm from './views/account-form'
import CustomStyle from './views/custom_style'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: Home,
      meta: { title: '首页' },
    },
    {
      name: 'add',
      path: '/add',
      component: AccountAdd,
      meta: { title: '添加新的OneDrive账号' },
      props: true,
    },
    {
      name: 'edit',
      path: '/edit/:id',
      component: AccountForm,
      meta: { title: '账号信息' },
    },
    {
      name: 'style_setting',
      path: '/style_setting',
      component: CustomStyle,
      meta: { title: '个性化设置' },
    },
    {
      name: '404',
      path: '',
      component: { template: '<h4>找不到对应的页面</h4>' },
      meta: { title: '找不到对应的页面' },
    },
  ],
})
