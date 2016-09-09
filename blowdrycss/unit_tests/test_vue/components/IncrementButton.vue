<template>
  <div class="text-align-center incremental">
    <h3 v-bind:class="cssclasses">Click to increment</h3>
    <button :class="cssclasses" @click.prevent="activate">+1</button>
  </div>
</template>

<script>
  import store from '../vuex-store'

  export default {
    data () {
      return {
        cssclasses: 'pink bold'
      }
    },
    methods: {
      activate () {
        store.dispatch('INCREMENT')
        console.log('+1 Pressed')
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
