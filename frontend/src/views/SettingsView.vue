<template>
  <div class="m-1 row">
    <div>
      <div class="d-inline m-1">
        <input type="button" value="Добавить/изменить пользователя" @click="is_edit_user">
      </div>
      <hr>
      <div class="d-inline m-1">
        <input type="button" value="Добавить предприятие (лабораторные исследования)" @click="is_create_research_enterprise">
      </div>
      <div class="d-inline m-1">
        <input type="button" value="Редактировать предприятие (лабораторные исследования)" @click="is_edit_enterprise">
      </div>
      <hr>
      <div class="d-inline m-1">
        <input type="button" value="Изменить список предприятий (всэ)" @click="is_create_vse_enterprise">
      </div>
      <div class="d-inline m-1">
        <input type="button" value="Изменить список показателей ВСЭ" @click="is_edit_vse">
      </div>
      <div class="d-inline m-1">
        <input type="button" value="Изменить цели ВСЭ для продукции" @click="is_edit_vse_products">
      </div>
      <hr>
    </div>

    <CreateEnterprise v-if="state.is_create_research_enterprise"></CreateEnterprise>
    <EditEnterprise v-if="state.is_edit_enterprise"></EditEnterprise>
    <EditUser v-if="state.is_edit_user"></EditUser>
    <EditVseEnterprise v-if="state.is_create_vse_enterprise"></EditVseEnterprise>
    <EditVse v-if="state.is_edit_vse"></EditVse>
    <EditVseProducts v-if="state.is_edit_vse_products"></EditVseProducts>
  </div>
</template>

<script>
import {reactive} from "vue";
import EditUser from "@/components/EditUser.vue";
import CreateEnterprise from "@/components/CreateResearchEnterprise.vue";
import EditEnterprise from "@/components/EditEnterprise.vue";
import EditVseEnterprise from "@/components/EditVseEnterprises.vue";
import EditVse from "@/components/EditVse.vue";
import EditVseProducts from "@/components/EditVseProducts.vue";

export default {
  name: "SettingsView",
  components: {EditVseProducts, EditVse, EditVseEnterprise, EditEnterprise, CreateEnterprise, EditUser},

  setup() {
    const state = reactive({
      is_create_research_enterprise: false,
      is_create_vse_enterprise: false,
      is_edit_enterprise: false,
      is_edit_user: false,
      is_edit_vse: false,
      is_edit_vse_products: false,
    })

    function is_create_research_enterprise() {
      state.is_create_research_enterprise = !state.is_create_research_enterprise
      state.is_edit_enterprise = false
      state.is_edit_user = false
      state.is_create_vse_enterprise = false
      state.is_edit_vse = false
      state.is_edit_vse_products = false
    }

    function is_edit_enterprise() {
      state.is_edit_enterprise = !state.is_edit_enterprise
      state.is_create_research_enterprise = false
      state.is_edit_user = false
      state.is_create_vse_enterprise = false
      state.is_edit_vse = false
      state.is_edit_vse_products = false
    }

    function is_edit_user() {
      state.is_edit_user = !state.is_edit_user
      state.is_create_research_enterprise = false
      state.is_edit_enterprise = false
      state.is_create_vse_enterprise = false
      state.is_edit_vse = false
      state.is_edit_vse_products = false
    }

    function is_create_vse_enterprise() {
      state.is_create_vse_enterprise = !state.is_create_vse_enterprise
      state.is_create_research_enterprise = false
      state.is_edit_enterprise = false
      state.is_edit_user = false
      state.is_edit_vse = false
      state.is_edit_vse_products = false
    }

    function is_edit_vse() {
      state.is_edit_vse = !state.is_edit_vse
      state.is_create_vse_enterprise = false
      state.is_create_research_enterprise = false
      state.is_edit_enterprise = false
      state.is_edit_user = false
      state.is_edit_vse_products = false
    }

    function is_edit_vse_products() {
      state.is_edit_vse_products = !state.is_edit_vse_products
      state.is_edit_vse = false
      state.is_create_vse_enterprise = false
      state.is_create_research_enterprise = false
      state.is_edit_enterprise = false
      state.is_edit_user = false
    }

    return {
      state,
      is_edit_enterprise,
      is_create_research_enterprise,
      is_create_vse_enterprise,
      is_edit_vse_products,
      is_edit_user,
      is_edit_vse,
    }
  }
}

</script>

<style scoped>
p {
  margin-bottom: 0;
}
</style>