<template>
    <v-app>
        <app-header />
        <v-content>
            <router-view />
        </v-content>
    </v-app>
</template>

<script>
import AppHeader from "@/views/AppHeader";
export default {
  name: "layout",
  components: {
    AppHeader,
  }
};
</script>
