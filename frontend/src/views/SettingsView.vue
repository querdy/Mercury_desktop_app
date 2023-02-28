<template>
  <div class="m-1 row">
    <div>
      <div class="d-inline m-1">
        <input type="button" value="Зарегистрировать предприятие" @click="is_create_enterprise">
      </div>
      <div class="d-inline m-1">
        <input type="button" value="Редактировать предприятие" @click="is_edit_enterprise">
      </div>
      <div class="d-inline m-1">
        <input type="button" value="Добавить/изменить пользователя" @click="is_edit_user">
      </div>
    </div>

    <CreateEnterprise v-if="state.is_create_enterprise"></CreateEnterprise>
    <EditEnterprise v-if="state.is_edit_enterprise"></EditEnterprise>
    <EditUser v-if="state.is_edit_user"></EditUser>
  </div>
</template>

<script>
import {reactive} from "vue";
import axios from "axios";
import EditUser from "@/components/EditUser.vue";
import CreateEnterprise from "@/components/CreateEnterprise.vue";
import EditEnterprise from "@/components/EditEnterprise.vue";

export default {
  name: "SettingsView",
  components: {EditEnterprise, CreateEnterprise, EditUser},

  setup() {
    const state = reactive({
      is_create_enterprise: false,
      is_edit_enterprise: false,
      is_edit_user: false,
    })

    function is_create_enterprise() {
      state.is_create_enterprise = !state.is_create_enterprise
      state.is_edit_enterprise = false
      state.is_edit_user = false
    }

    function is_edit_enterprise() {
      state.is_edit_enterprise = !state.is_edit_enterprise
      state.is_create_enterprise = false
      state.is_edit_user = false
    }

    function is_edit_user() {
      state.is_edit_user = !state.is_edit_user
      state.is_create_enterprise = false
      state.is_edit_enterprise = false
    }

    return {
      state,
      is_edit_enterprise,
      is_create_enterprise,
      is_edit_user,
    }
  }
}

</script>

<style scoped>
p {
  margin-bottom: 0;
}
</style>