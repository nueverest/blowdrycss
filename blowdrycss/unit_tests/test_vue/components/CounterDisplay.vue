<template>
  <div class="blue testing-123">
    Count is {{ count }}
  </div>
</template>

<script>
  import store from '../vuex-store'

  export default {
    computed: {
      count () {
        console.log(store.state.counter)
        return store.state.counter
      }
    }
  }
</script>

<style scoped></style>
