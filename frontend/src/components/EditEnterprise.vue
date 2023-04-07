<template>
  <div>
    <select id="enterpriseSelect" class="m-1" style="height: 30px" v-model="state.selected_uuid"
            @change="set_edited_enterprise(state.selected_uuid)">
      <option disabled value="null">Выберите предприятие</option>
      <option :value="enterprise.uuid" v-for="enterprise in state.enterprises" :key="enterprise">{{
          enterprise.name
        }}
      </option>
    </select>
    <div v-if="state.selected_uuid">
      <table class="m-1 table table-bordered table-sm">
        <thead>
        <tr>
          <th>Продукт</th>
          <th>лаборатория</th>
          <th>Показатель</th>
          <th>Дата иссл.</th>
          <th>Метод иссл.*</th>
          <th>Номер эксп.</th>
          <th>Результат</th>
          <th>Заключение</th>
        </tr>
        </thead>
        <tbody>
        <tr :key="'research-'+indexResearch" v-for="(research, indexResearch) in state.edited_enterprise.researches">
          <td>
            <input class="table-input" type="text" v-model="state.edited_enterprise.researches[indexResearch].product">
<!--                <textarea rows="3" v-model="state.edited_enterprise.researches[indexResearch].product"></textarea>-->
          </td>
          <td>
            <input class="table-input" type="text"
                   v-model="state.edited_enterprise.researches[indexResearch].laboratory">
          </td>
          <td>
            <input class="table-input" type="text" v-model="state.edited_enterprise.researches[indexResearch].disease">
          </td>
          <td style="width: 10%">
            <input class="table-input" type="text"
                   v-model="state.edited_enterprise.researches[indexResearch].dateOfResearch"></td>
          <td style="width: 7%">
            <input class="table-input" type="text" v-model="state.edited_enterprise.researches[indexResearch].method">
          </td>
          <td>
            <input class="table-input" type="text"
                   v-model="state.edited_enterprise.researches[indexResearch].expertiseId">
          </td>
          <td style="width: 7%">
            <select style="height: 27px;" v-model="state.edited_enterprise.researches[indexResearch].result">
              <option disabled value="">Выберите</option>
              <option value="1">Positive</option>
              <option value="2">Negative</option>
              <option value="3">N/A</option>
            </select></td>
          <td>
            <input class="table-input" type="text"
                   v-model="state.edited_enterprise.researches[indexResearch].conclusion">
          </td>
          <td>
            <input class="align-middle m-1" type="image" v-bind:src="require('/src/assets/cross.png')" alt="cross"
                   height="25" width="25" @click="delete_item(indexResearch)">
          </td>
        </tr>
        </tbody>
      </table>
    </div>
    <div class="d-inline m-1">
      <input v-if="state.edited_enterprise.name" type="button" value="Добавить исследование"
             @click="append_edited_research">
    </div>
    <hr v-if="state.edited_enterprise.name">
    <div v-if="state.edited_enterprise.name">
      <input class="m-1" type="button" @click="update_enterprise" value="Сохранить">
      <input class="m-1" type="button" @click="delete_enterprise" value="Удалить предприятие">
    </div>
  </div>
</template>

<script setup>
import {reactive} from "vue";
import axios from "axios";
import {useNotification} from "@kyvg/vue3-notification";

const {notify} = useNotification()

const state = reactive({
  selected_uuid: null,
  enterprises: [],
  edited_enterprise: {},
})

const emptyResearch = {
  product: 'main',
  laboratory: '',
  disease: '',
  dateOfResearch: '',
  method: '',
  expertiseId: '',
  result: '',
  conclusion: '',
}

axios.get("http://localhost:8000/api/v1/research/enterprises")
    .then((response) => {
      state.enterprises = response.data
    })

function set_edited_enterprise(uuid) {
  state.enterprises.forEach((enterprise) => {
    if (enterprise.uuid === uuid) {
      state.edited_enterprise = enterprise
    }
  })
}

function delete_item(index) {
  state.edited_enterprise.researches.splice(index, 1)
}

function append_edited_research() {
  let newResearch = JSON.parse(JSON.stringify(emptyResearch))
  state.edited_enterprise.researches.push(newResearch)
}

function update_enterprise() {
  axios.put("http://localhost:8000/api/v1/research/enterprise", state.edited_enterprise)
      .then(() => {
        notify({
          type: "success",
          text: "Изменения внесены успешно",
        });
      })
      .catch(() => {
        notify({
          type: "error",
          text: "Не удалось внести изменения",
        });
      })
}

function delete_enterprise() {
  axios.delete("http://localhost:8000/api/v1/research/enterprise", {
        data:
            {"uuid": state.selected_uuid}
      }
  )
      .then(() => {
        notify({
          type: "success",
          text: "Предприятие удалено",
        });
      })
      .catch(() => {
        notify({
          type: "error",
          text: "Не удалось удалить предприятие",
        });
      })
}

</script>

<style scoped>
.table-input {
  width: 100%;
}

.table {
  font-size: 14px;
  white-space: nowrap;
}

p {
  margin-bottom: 0;
}

#enterpriseSelect {
  width: 25%;
  /*height: 30px;*/
}
</style>