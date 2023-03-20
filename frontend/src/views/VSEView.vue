<template>
  <div class="m-1 row">
    <div id="transaction_input" class="col-12">
      <label class="m-1">Номер транзакции: </label>
      <input class="m-1" type="text" @input="updateInput">
      <select class="mx-1" style="height: 30px" v-model="state.selected_enterprise">
        <option value="" selected disabled>Выберите</option>
        <option :value="enterprise.mercuryId" v-for="enterprise in state.enterprises" :key="enterprise">{{
            enterprise.name
          }}
        </option>
      </select>
      <input class="m-1" type="button" value="Старт!" @click="startIsClicked">
      <LoadingView class="m-1 mx-2" :is-loading="state.isLoading"/>
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
  name: "VSEView",
  components: {LoadingView},
  setup() {
    const state = reactive({
      isLoading: false,
      input_transaction_pk: '',
      selected_enterprise: '',
    })
    axios.get("http://127.0.0.1:8000/api/v1/vse/enterprise")
        .then((response) => {
          state.enterprises = response.data
        })

    function updateInput(event) {
      state.input_transaction_pk = event.target.value
    }

    function startIsClicked() {
      state.isLoading = true
      axios.post("http://127.0.0.1:8000/api/v1/vse/push_vse", {
        "enterprisePk": state.selected_enterprise,
        "transactionPk": state.input_transaction_pk,
      })
          .then(() => {
            state.isLoading = false
            notify({
              type: "success",
              text: "Запущено внесение ВСЭ",
            });

          })
          .catch(() => {
            state.isLoading = false
            notify({
              type: "error",
              text: "Не удалось запустить внесение ВСЭ",
            });
          })
    }

    return {
      state,
      updateInput,
      startIsClicked,
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
}
</style>