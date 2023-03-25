<template>
  <div>
    <div>
      <p class="d-inline">Логика работы таблицы исследований: </p>
      <p class="d-inline">
        <input class="" type="button" data-bs-toggle="collapse" data-bs-target="#clue"
               aria-expanded="false" aria-controls="clue" value="Скрыть/Показать" style="height: 20px; font-size: 10px">
      </p>
    </div>
    <div class="collapse" id="clue">
      <p>1. Если Продукт указан как 'main' - это исследование вносится на всю продукцию, кроме той которая указана в
        других строках</p>
      <p>2. Если Продукт указан (точное наименование продукции из Меркурия) - исследование вносится только на продукты
        с
        этим названием</p>
      <p>3. Если указан Продукт, но не заполнено хотя бы одно обязательное поле ('*' - необязательные поля) -
        исследования
        не вносятся на продукцию с данным наименованием</p>
    </div>
    <hr>
    <div>
      <label class="m-1">Название предприятия: </label>
      <input class="m-1" v-model="state.enterprise.name">
    </div>
    <div v-if="state.enterprise.name">
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
        <tr :key="'research-'+indexResearch" v-for="(research, indexResearch) in state.enterprise.researches">
          <td><input class="table-input" type="text" v-model="state.enterprise.researches[indexResearch].product">
          </td>
          <td><input class="table-input" type="text" v-model="state.enterprise.researches[indexResearch].laboratory">
          </td>
          <td><input class="table-input" type="text" v-model="state.enterprise.researches[indexResearch].disease">
          </td>
          <td><input class="table-input" type="text"
                     v-model="state.enterprise.researches[indexResearch].dateOfResearch"></td>
          <td><input class="table-input" type="text" v-model="state.enterprise.researches[indexResearch].method"></td>
          <td><input class="table-input" type="text" v-model="state.enterprise.researches[indexResearch].expertiseId">
          </td>
          <td><select style="height: 27px" v-model="state.enterprise.researches[indexResearch].result">
            <option disabled value="">Выберите</option>
            <option value="1">Positive</option>
            <option value="2">Negative</option>
            <option value="3">N/A</option>
          </select></td>
          <td><input class="table-input" type="text" v-model="state.enterprise.researches[indexResearch].conclusion">
          </td>
          <td>
            <input class="align-middle m-1" type="image" v-bind:src="require('/src/assets/cross.png')" alt="cross"
                   height="25" width="25" @click="delete_item(indexResearch)">
          </td>
        </tr>
        </tbody>
      </table>
    </div>
    <div>
      <div class="d-inline m-1">
        <input v-if="state.enterprise.name" type="button" value="Добавить исследование" @click="append_research">
      </div>
      <!--      <div class="d-inline m-1">-->
      <!--        <input v-if="state.enterprise.name" type="button" value="Удалить исследование" @click="pop_research">-->
      <!--      </div>-->
    </div>
    <hr v-if="state.enterprise.name">
    <div class="m-1" v-if="state.enterprise.name">
      <input type="button" value="Сохранить" @click="create_enterprise">
    </div>
  </div>
</template>

<script setup>
import {reactive} from "vue";
import axios from "axios";
import {useNotification} from "@kyvg/vue3-notification";

const {notify} = useNotification()

const state = reactive({
  enterprise: {
    name: '',
    researches: [
      {
        product: 'main',
        laboratory: '',
        disease: '',
        dateOfResearch: '',
        method: '',
        expertiseId: '',
        result: '',
        conclusion: ''
      },
    ],
  },
  emptyResearch: {
    product: 'main',
    laboratory: '',
    disease: '',
    dateOfResearch: '',
    method: '',
    expertiseId: '',
    result: '',
    conclusion: '',
  },
})

function append_research() {
  let newResearch = JSON.parse(JSON.stringify(state.emptyResearch))
  state.enterprise.researches.push(newResearch)
}

function delete_item(index) {
  state.enterprise.researches.splice(index, 1)
}

function create_enterprise() {
  axios.post('http://127.0.0.1:8000/api/v1/research/enterprise', state.enterprise)
      .then(() => {
        state.enterprise.name = ''
        state.enterprise.researches = []
        append_research()
        notify({
          type: "success",
          text: "Предприятие успешно создано",
        });
      })
      .catch(() => {
        notify({
          type: "error",
          text: "Не удалось создать предприятие",
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
</style>