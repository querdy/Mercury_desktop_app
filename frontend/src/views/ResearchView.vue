<template>

  <div class="m-1 row">

    <div id="transaction_input" class="col-12">
      <label class="m-1">Номер транзакции: </label>
      <input class="m-1" type="text" @input="updateInput">
      <select class="mx-1" style="height: 30px" v-model="state.selected_enterprise">
        <option value="" selected disabled>Выберите</option>
        <option :value="enterprise.uuid" v-for="enterprise in state.enterprises" :key="enterprise">{{
            enterprise.name
          }}
        </option>
      </select>
      <input class="m-1" type="button" value="Старт!" @click="startIsClicked">
      <LoadingView class="m-1 mx-2" :is-loading="state.isLoading"/>
    </div>
    <div class="m-1 position-static">
      <div v-if="state.returned_transaction.transactionPk > 0">
        Получены записи журнала для транзакции: {{ state.returned_transaction.transactionPk }}
        <div class="border-bottom" v-for="traffic in state.traffics" :key="traffic.traffic">
          <div class="row">
            <div class="col-2 d-inline">{{ traffic.traffic }}</div>
            <div class="col-4 d-inline">{{ traffic.productName }}</div>
            <div class="col-2 d-inline">{{ traffic.status }}</div>
          </div>
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
  name: "ResearchView",
  components: {LoadingView},
  setup() {
    const state = reactive({
      isLoading: false,
      input_transaction_pk: '',
      selected_enterprise: '',
      returned_transaction: {},
      traffics: [],
      enterprises: {},
    })
    axios.get("http://127.0.0.1:8000/api/v1/research/enterprises")
        .then((response) => {
          state.enterprises = response.data
        })


    function updateInput(event) {
      state.input_transaction_pk = event.target.value
    }

    function startIsClicked() {
      state.complete = []
      state.isLoading = true
      axios.get('http://127.0.0.1:8000/api/v1/research/' + state.input_transaction_pk + '/' + state.selected_enterprise)
          .then((response) => {
            state.returned_transaction = response.data;
            state.traffics = response.data.traffics;
            state.isLoading = false
            notify({
              type: "success",
              text: "Запущено внесение исследований",
            });
            state.traffics.forEach(traffic => {
              axios.post('http://127.0.0.1:8000/api/v1/research/push_research', {
                'enterpriseUuid': state.selected_enterprise,
                'transactionPk': state.returned_transaction.transactionPk,
                'traffic': {
                  'traffic': traffic.traffic,
                  'productName': traffic.productName,
                  'status': traffic.status,
                }
              })
                  .then((response) => {
                    state.traffics.forEach(traffic => {
                      if (traffic.traffic === response.data.traffic) {
                        traffic.status = response.data.status
                      }
                    })
                    state.traffics[response.data.traffic] = response.data.traffic.status;
                  })
            })
          })
          .catch(() => {
            state.isLoading = false
            notify({
              type: "error",
              text: "Не удалось запустить внесение исследований",
            });
          })
    }

    return {
      state,
      updateInput,
      startIsClicked
    }
  }
}
</script>

<style scoped>
p {
  display: inline-block;
}

#transaction_input {
  text-align: left;
  /*margin: 10px;*/
}

.string_input {
  margin: 5px;
}

.label {
  margin: 5px;
}
</style>