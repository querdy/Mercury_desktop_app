<template>
  <div class="row">
    <div class="col-6">
      <table class="m-1 table table-bordered table-sm">
        <thead>
        <tr>
          <th>Название предприятия</th>
          <th>Номер предприятия в реестре</th>
        </tr>
        </thead>
        <tbody>
        <tr :key="'enterprise'+index" v-for="(enterprise, index) in state.enterprises">
          <td>
            <input class="table-input" type="text" v-model="state.enterprises[index].name">
          </td>
          <td>
            RU <input class="table-input" style="width: 85%" type="text" v-model="state.enterprises[index].mercuryId">
          </td>
          <td>
            <input class="align-middle m-1" type="image" v-bind:src="require('/src/assets/cross.png')" alt="cross" height="25" width="25" @click="delete_item(index)">
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div class="d-inline m-1">
    <input type="button" value="Добавить предприятие" @click="append_enterprise">
  </div>
  <div class="d-inline m-1">
    <input type="button" @click="push_update" value="Сохранить">
  </div>
</template>

<script>
import {reactive} from "vue";
import axios from "axios";
import {useNotification} from "@kyvg/vue3-notification";
const { notify}  = useNotification()

export default {
  name: "EditVseEnterprises",

  setup() {
    const state = reactive({
      enterprises: [],
      emptyEnterprise: {
        uuid: null,
        name: '',
        mercuryId: '',
      }
    })

    axios.get("http://127.0.0.1:8000/api/v1/vse/enterprise")
        .then((response) => {
          state.enterprises = response.data
        })

    function append_enterprise() {
      let newEnterprise = JSON.parse(JSON.stringify(state.emptyEnterprise))
      state.enterprises.push(newEnterprise)
    }

    function delete_item(index) {
      state.enterprises.splice(index, 1)
    }

    function push_update() {
      axios.post("http://127.0.0.1:8000/api/v1/vse/enterprise", {"enterprises": state.enterprises})
          .then((response) => {
            if (response.status === 201) {
              notify({
                type: "success",
                text: "Список предприятий спешно изменен",
              });
            }
          })
    }

    return {
      state,
      append_enterprise,
      delete_item,
      push_update,
    }
  }
}
</script>

<style scoped>
</style>