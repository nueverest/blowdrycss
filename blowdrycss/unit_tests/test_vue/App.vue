<template>
  <div>
    <h3>Increment:</h3>
    <increment></increment>
    <h3>Counter:</h3>
    <counter></counter>
  </div>
</template>

<script>
  import { default as counter } from './components/CounterDisplay.vue'
  import { default as increment } from './components/IncrementButton.vue'

  export default {
    components: {
      counter,
      increment
    }
  }
</script>

<style scoped></style>
