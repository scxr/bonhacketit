// auth/register.html

let app = new Vue({
  delimiters: ["${", "}"],
  el: "#app",
  data: {
    message: {},
    username: "",
    password: "",
    confirm_password: "",
  },
  created() {
    // redirect if user already logged in
    if (getUsername()) {
      location.replace("/");
    }
  },
  methods: {
    async register() {
      if (!this.username && !this.password) {
        this.message = {
          status: "warning",
          text: "enter a username",
        };
        return;
      }
      if (this.password !== this.confirm_password) {
        this.message = {
          status: "warning",
          text: "passwords dont match",
        };
        return;
      }

      const response = await fetch("/register", {
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
        location.replace("/");
        this.message = {
          status: "success",
          text: "successfully registered",
        };
      }
    },
  },
});
