import {reactive} from "vue";
import axios from "axios";

export const activeUserState = reactive({
    user: "",
})

getActiveUser()

export function getActiveUser() {
    axios.get("http://localhost:8000/api/v1/user/active")
        .then((response) => {
            activeUserState.user = response.data.login
        })
}