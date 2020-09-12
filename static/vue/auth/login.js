// auth/login.html

let app = new Vue({
  delimiters: ["${", "}"],
  el: "#app",
  data: {
    message: {},
    username: "",
    password: "",
  },
  created() {
    // redirect if user already logged in
    if (getUsername()) {
      location.replace("/");
    }
  },
  methods: {
    async login() {
      if (!this.username && !this.password) {
        this.message = {
          status: "warning",
          text: "enter a username",
        };
        return;
      }

      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      });

      const data = await response.json();

      if (data.error) {
        this.message = {
          status: "danger",
          text: data.error,
        };
      } else {
        // redirect to home page
        location.href = "/";
        this.message = {
          status: "success",
          text: "successfully registered",
        };
      }
    },
  },
});
