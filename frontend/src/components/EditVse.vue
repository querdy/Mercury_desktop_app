<template>
  <div class="row">
    <div class="col-12">
      <div class="col-12">
        <label class="m-1">Номер транзакции: </label>
        <input class="m-1" type="text" v-model="state.input_traffic">
        <select class="m-1" style="height: 30px" v-model="state.selected_enterprise">
          <option value="" selected disabled>Выберите</option>
          <option :value="enterprise.mercuryId" v-for="enterprise in state.enterprises" :key="enterprise">{{
              enterprise.name
            }}
          </option>
        </select>
        <input class="m-1" type="button" value="Собрать данные о продукции" @click="startIsClicked">
        <LoadingView class="m-1 mx-2" :is-loading="state.isLoading"/>
      </div>
      <table class="m-1 table table-bordered table-sm">
        <thead>
        <tr>
          <th>Продукт</th>
          <th>Показатель</th>
          <th>Фактич. знач.</th>
          <th>Заключение</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(vse_param, index) in state.active_vse_params" :key="'vse-param-'+index">
          <td>
            <select v-model="state.active_vse_params[index].productName">
              <option  :key="'product-'+product.uuid" v-for="product in state.products" :value="product.productName">{{ product.productName }}</option>
            </select>
          </td>
          <td>
            <select v-model="state.active_vse_params[index].view" @change="change_param_value(index)">
              <option :key="'view-'+product.uuid"
                      v-for="product in state.vse_params[state.active_vse_params[index].productName]"
                      :value="product.view">{{ product.view }}
              </option>
            </select>
          </td>
          <td>
            <input class="table-input" type="text" v-model="state.active_vse_params[index].factValue">
          </td>
          <td>
            <input class="table-input" type="text" v-model="state.active_vse_params[index].conclusion">
          </td>
          <td>
            <input class="align-middle m-1" type="image" v-bind:src="require('/src/assets/cross.png')" alt="cross"
                   height="25" width="25" @click="delete_item(index)">
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="d-inline m-1">
    <input type="button" value="Добавить всэ" @click="append_active_vse_param">
  </div>
  <div class="d-inline m-1">
    <input type="button" @click="push_update" value="Сохранить">
  </div>
</template>

<script>
import {reactive} from "vue";
import axios from "axios";
import {useNotification} from "@kyvg/vue3-notification";
import LoadingView from "@/components/LoadingView.vue";

const {notify} = useNotification()

export default {
  name: "EditVse",
  components: {LoadingView},

  setup() {
    const state = reactive({
      isLoading: false,
      input_traffic: '',
      enterprises: [],
      selected_enterprise: '',
      products: [],
      active_vse_params: [],
      vse_params: {},
      emptyVseParam: {
        uuid: null,
        value: null,
        view: null,
        factValue: 'Соответствует НД',
        conclusion: 'Соответствует НД',
        productName: null,
      },

    })

    get_params()

    function get_params() {
      axios.get("http://localhost:8000/api/v1/vse/product")
          .then((response) => {
            state.products = response.data.products
          })
      axios.get("http://localhost:8000/api/v1/vse/active_vse_param")
          .then((response) => {
            state.active_vse_params = response.data.activeVseParams
          })
      axios.get("http://localhost:8000/api/v1/vse/vse_param")
          .then((response) => {
            state.vse_params = response.data.vseParams
          })
      axios.get("http://127.0.0.1:8000/api/v1/vse/enterprise")
          .then((response) => {
            state.enterprises = response.data
          })
    }

    function append_active_vse_param() {
      let newActiveVseParam = JSON.parse(JSON.stringify(state.emptyVseParam))
      state.active_vse_params.push(newActiveVseParam)
    }

    function delete_item(index) {
      state.active_vse_params.splice(index, 1)
    }

    function push_update() {
      axios.post("http://127.0.0.1:8000/api/v1/vse/active_vse_param", {"active_vse_params": state.active_vse_params})
          .then((response) => {
            if (response.status === 201) {
              notify({
                type: "success",
                text: "Список всэ успешно изменен",
              });
            }
          })
    }

    function startIsClicked() {
      state.isLoading = true
      axios.get("http://127.0.0.1:8000/api/v1/vse/vse_param/" + state.input_traffic + "/" + state.selected_enterprise)
          .then((response) => {
            if (response.status === 200) {
              notify({
                type: "success",
                text: "Список продукции получен",
              });
            }
          })
          .catch(() => {
            notify({
              type: "error",
              text: "Не удалось получить данные",
            });
          })
          .finally(() => {
            get_params()
            state.isLoading = false
          })
    }

    function change_param_value(index) {
      let productName = state.active_vse_params[index].productName
      state.vse_params[productName].forEach(item => {
        if (item.view === state.active_vse_params[index].view) {
          state.active_vse_params[index].value = item.value
        }
      })
    }

    return {
      state,
      append_active_vse_param,
      startIsClicked,
      delete_item,
      push_update,
      change_param_value,
    }
  }

}
</script>

<style scoped>
td select {
  width: 100%;
  height: 30px;
}

td {
  width: 25%;
}

.table-input {
  width: 100%;
}
</style>