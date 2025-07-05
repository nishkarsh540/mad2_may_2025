<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">PASSWORD:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
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
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post("http://127.0.0.1:5000/login", {
          username: this.username,
          password: this.password,
        });
        const { access_token, user } = response.data;
        console.log(user);
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("user", JSON.stringify(user));

        if (user.role === "admin") {
          this.$router.push("/admin-dashboard");
        } else {
          this.$router.push("/user-dashboard");
        }
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
