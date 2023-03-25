<template>
  <div class="row">
    <div class="col-12">
      <div class="d-inline m-1">
        <input type="button" @click="push_update" value="Сохранить">
      </div>
      <table class="m-1 table table-bordered table-sm">
        <thead>
        <tr>
          <th>uuid</th>
          <th>Продукт</th>
          <th>Цель</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(product, index) in state.products" :key="'product'+product.uuid">
          <td>
            {{ product.uuid }}
          </td>
          <td>
            {{ product.productName }}
          </td>
          <td>
            <select v-model="state.products[index].vseTarget">
              <option :key="'target'-target.value" v-for="target in state.targets" :value="target.value">{{
                  target.view
                }}
              </option>
            </select>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import {reactive} from "vue";
import axios from "axios";
import {useNotification} from "@kyvg/vue3-notification";

const {notify} = useNotification()

const state = reactive({
  products: Array,
  targets: Array,
})

axios.get("http://localhost:8000/api/v1/vse/product")
    .then((response) => {
      state.products = response.data.products
    })

axios.get("http://localhost:8000/api/v1/vse/vse_target")
    .then((response) => {
      state.targets = response.data.targets
    })

function push_update() {
  axios.put("http://127.0.0.1:8000/api/v1/vse/vse_target", {"products": state.products})
      .then((response) => {
        if (response.status === 200) {
          notify({
            type: "success",
            text: "Список целей всэ успешно изменен",
          });
        }
      })
}

</script>

<style scoped>
td select {
  width: 100%;
  height: 30px;
}
</style>