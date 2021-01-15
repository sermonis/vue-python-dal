import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

/* Layout */
import Layout from "@/layout";

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
    {
        path: "/login",
        component: () => import("@/views/login/index"),
        hidden: true,
    },

    {
        path: "/404",
        component: () => import("@/views/404"),
        hidden: true,
    },

    {
        path: "/my-materials/",
        component: Layout,
        children: [
            {
                path: "",
                name: "Мои материалы",
                component: () => import("@/views/myMaterials/index"),
                meta: {title: "Мои материалы", icon: ""},
            },
        ],
    },

    {
        path: "/",
        component: Layout,
        redirect: "/msw/science-articles",
        name: "Military scientific work",
        children: [
            {
                path: "/msw/science-articles",
                name: "Science Articles",
                component: () => import("@/views/ScienceArticles/index"),
                meta: {title: "Военно-научные работы", icon: ""},
            },
        ],
    },
    {
        path: "/subjects/",
        component: Layout,
        children: [
            {
                path: "",
                name: "Subjects",
                component: () => import("@/views/Subjects/index"),
                meta: {title: "Учебно-методические материалы", icon: ""},
            },
            {
                path: "/subjects/:subjectId/",
                hidden: true,
                name: "Subject",
                component: () => import("@/views/Subject/index"),
                meta: {title: "Учебно-методические материалы", icon: ""},
            },
        ],
    },
    {
        path: "/library/",
        component: Layout,
        children: [
            {
                path: "",
                name: "Library",
                component: () => import("@/views/Library/index"),
                meta: {title: "Электронная библиотека", icon: ""},
            },
        ],
    },

    {
        path: "/personnel",
        component: Layout,
        children: [
            {
                path: "",
                name: "Personnel",
                component: () => import("@/views/Personnel/index"),
                meta: {title: "Личный состав ВУЦ", icon: ""},
            },
        ],
    },

    {
        path: "/absence",
        component: Layout,
        children: [
            {
                path: "",
                name: "Absence",
                component: () => import("@/views/Absence/index"),
                meta: {title: "Журнал посещаемости", icon: ""},
            },
        ],
    },

    {
        path: "/discipline",
        component: Layout,
        children: [
            {
                path: "",
                name: "Discipline",
                component: () => import("@/views/Discipline/index"),
                meta: {title: "Дисциплинарный журнал", icon: ""},
            },
        ],
    },

    // {
    //   path: '/mtc_referencebook',
    //   redirect: '/referencebook',
    //   component: Layout,
    //   children: [{
    //     path: 'referencebook',
    //     name: 'ReferenceBook',
    //     component: () => import('@/views/ReferenceBook/index'),
    //     meta: { title: 'Справочники', icon: '' }
    //   }]
    // },

    // {
    //   path: 'external-link',
    //   component: Layout,
    //   children: [
    //     {
    //       path: 'https://panjiachen.github.io/vue-element-admin-site/#/',
    //       meta: { title: 'External Link', icon: 'link' }
    //     }
    //   ]
    // },

    // 404 page must be placed at the end !!!

    {path: "*", redirect: "/404", hidden: true},
];

const createRouter = () =>
    new Router({
        // mode: 'history', // require service support
        scrollBehavior: () => ({y: 0}),
        routes: constantRoutes,
    });

const router = createRouter();

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
    const newRouter = createRouter();
    router.matcher = newRouter.matcher; // reset router
}

export default router;
