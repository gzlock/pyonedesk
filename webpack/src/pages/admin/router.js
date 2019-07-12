import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/home'
import AccountAdd from './views/account-add'
import AccountForm from './views/account-form'

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
    /*{
      name: '500',
      path: '/500',
      component: {template: '<h4>服务器在查询时发生了错误</h4>'},
      meta: {title: '服务器在查询时发生了错误'}
    },
    {
      name: '404',
      path: '/404',
      component: {template: '<h4>找不到对应的数据</h4>'},
      meta: {title: '找不到对应的数据'}
    },
    {
      name: '404',
      path: '',
      component: {template: '<h4>找不到对应的数据</h4>'},
      meta: {title: '找不到对应的数据'}
    },*/
  ],
})
