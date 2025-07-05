<template>
  <div>
    <h2>Signup</h2>
    <form @submit.prevent="signupUser">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">PASSWORD:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Signup</button>
    </form>
    <div v-if="errorMessage">{{ errorMessage }}</div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async signupUser() {
      try {
        await axios.post("http://127.0.0.1:5000/signup", {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        this.$router.push("/login");
      } catch (error) {
        this.errorMessage = error.response
          ? error.response.data.message
          : "An error occurred during signup.";
      }
    },
  },
};
</script>

<style scoped></style>
