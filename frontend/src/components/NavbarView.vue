<template>
  <div class="d-flex align-items-center sticky-top bg-light font-monospace">
    <nav class="p-0 navbar navbar-expand-lg">
        <ul class="navbar-nav">
          <li class="nav-item mx-1">
            <router-link to="/">Research</router-link>
          </li>
          <li class="nav-item mx-1">
            <router-link to="/vse">VSE</router-link>
          </li>
<!--          <li class="nav-item mx-1">-->
<!--            <router-link to="/rawmilk">RawMilk</router-link>-->
<!--          </li>-->
          <li class="nav-item mx-1">
            <router-link to="/settings">Settings</router-link>
          </li>
        </ul>
    </nav>
    <div class="mx-1">
      | Активный пользователь: <i>{{ activeUserState.user }}</i>
    </div>
  </div>
</template>

<script setup>
import {activeUserState} from "@/components/ActiveUser";
</script>

<style scoped>

nav a {
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
}

nav a::after {
  content: '';
  display: block;
  left: 0;
  width: 0;
  background-color: #495057;
  height: 1px;
  transition: all .5s;
}

nav a:hover:after {
  width: 100%;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>