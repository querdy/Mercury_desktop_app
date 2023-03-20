<template>
  <nav class="sticky-top bg-light">
    |
    <router-link to="/">Research</router-link>
    |
    <router-link to="/vse">VSE</router-link>
    |
    <router-link to="/settings">Settings</router-link>
    |
  </nav>
</template>

<script>
export default {
  name: "NavbarView"
}
</script>

<style scoped>
nav {
  padding: 10px;
  /*background-color: gray;*/
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>