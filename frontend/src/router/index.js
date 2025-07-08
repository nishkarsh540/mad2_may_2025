import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserSignup from '../auth/UserSignup.vue'
import UserLogin from '../auth/UserLogin.vue'
import CategoryManage from '@/components/CategoryManage.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/signup',
    name: 'signup',
    component: UserSignup
  },
  {
    path: '/login',
    name: 'login',
    component: UserLogin
  },
  {
    path: '/manage_cat',
    name: 'Manage Category',
    component: CategoryManage,
    meta: { isAdmin: true }
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
    meta: { isAdmin: true}
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to,from,next) =>{
  const userRole = JSON.parse(localStorage.getItem('user')).role || 'guest'
  if (to.meta.isAdmin && userRole !== 'admin') {
    next({path: '/login', query: {unauthorized: true}});
  } else {
    next();
  }
})


export default router
