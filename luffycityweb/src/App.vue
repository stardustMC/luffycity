<template>
<router-view></router-view>
</template>

<script setup>
import http from "./utils/http.js"

http.get("/home/test").then(response=> {
  console.log(response.data)
})
</script>

<style scoped>
body,h1,h2,h3,h4,p,table,tr,td,ul,li,a,form,input,select,option,textarea {
  margin: 0;
  padding: 0;
  font-size: 15px;
}

a{
  text-decoration: none;
  color: #333;
  cursor: pointer;
}

ul,li{
    list-style: none;
}

table{
  border-collapse: collapse;
}

img{
  max-height: 100%;
  max-width: 100%;
}

input{
  outline: none;
}
</style>
