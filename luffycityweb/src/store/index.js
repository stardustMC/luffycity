import {createStore} from "vuex"
import createPersistedState from "vuex-persistedstate"

const store = createStore({
    plugins: [createPersistedState()],
    state(){
        return {
            user: {

            }
        }
    },
    getters: {
        getUserInfo(state){
            // 从jwt的载荷中提取用户信息
            let now = parseInt( (new Date() - 0) / 1000 );
            if(state.user.exp === undefined) {
                // 没登录
                state.user = {}
                localStorage.token = null;
                sessionStorage.token = null;
                return null
            }

            if(parseInt(state.user.exp) < now) {
                // 过期处理
                state.user = {}
                localStorage.token = null;
                sessionStorage.token = null;
                return null
            }
            return state.user;
        }
    },
    mutations:{
        login(state, user){
            state.user = user;
        }
    }
})

export default store;