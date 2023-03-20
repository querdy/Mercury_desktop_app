<template>
  <div class="row">
    <div class="col-12">
      <div v-if="state.users.length !== 0">
        <label class="m-1">Пользователь: </label>
        <select class="m-1" style="height: 30px" v-model="state.selected_user">
          <option selected disabled value="">Выберите</option>
          <option :value="user.login" v-for="user in state.users" :key="user.uuid">{{ user.login }}</option>
        </select>
        <input class="m-1" type="button" value="Сделать активным" @click="switch_user">
        <input class="m-1" type="button" value="Удалить" @click="delete_user">
      </div>
      <hr class="m-1">
      <div class="">
        <div class="row">
          <label class="m-1 col-1">login: </label>
          <input class="m-1 col-2" type="text" v-model="state.user.login">
        </div>
        <div class="row">
          <label class="m-1 col-1">password: </label>
          <input class="m-1 col-2" type="text" v-model="state.user.password">
        </div>
        <div class="row m-1">
          <input class="col-2" type="button" value="Добавить" @click="update_user">
          <LoadingView class="m-1 mx-2" :is-loading="state.isLoading"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {reactive} from "vue";
import axios from "axios";
import LoadingView from "@/components/LoadingView.vue";
import {useNotification} from "@kyvg/vue3-notification";

const {notify} = useNotification()
export default {
  name: "EditUser",
  components: {LoadingView},

  setup() {
    const state = reactive({
      isLoading: false,
      user: {
        login: '',
        password: ''
      },
      users: [],
      selected_user: ''
    })

    function updateUserList() {
      axios.get("http://127.0.0.1:8000/api/v1/user/all")
          .then((response) => {
            state.users = response.data
          })
    }

    updateUserList()

    function update_user() {
      state.isLoading = true
      axios.post("http://127.0.0.1:8000/api/v1/user/check", state.user)
          .then(() => {
            notify({
              type: "success",
              text: "Авторизация прошла успешно",
            });
          })
          .catch(() => {
            notify({
              type: "error",
              text: "Неудачная авторизация",
            });
          })
          .finally(() => {
            state.isLoading = false
            updateUserList()
          })
    }

    function switch_user() {
      axios.get("http://127.0.0.1:8000/api/v1/user/set/" + state.selected_user)
          .then(() => {
            notify({
              type: "success",
              text: "Активный пользователь изменен на " + state.selected_user,
            });
          })
          .catch(() => {
            notify({
              type: "error",
              text: "Не удалось изменить активного пользователя",
            });
          })
    }

    function delete_user() {
      axios.delete("http://127.0.0.1:8000/api/v1/user/", {data: {"login": state.selected_user}})
          .then(() => {
            notify({
              type: "success",
              text: "Пользователь " + state.selected_user + " удален",
            });
          })
          .catch(() => {
            notify({
              type: "error",
              text: "Не удалось удалить пользователя. Обновите страницу и попробуйте снова",
            });
          })
          .finally(() => {
            updateUserList()
          })
    }

    return {
      state,
      update_user,
      switch_user,
      delete_user,
    }
  }
}
</script>

<style scoped>

</style>