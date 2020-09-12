// create_recipe.html

let home = new Vue({
  delimiters: ["${", "}"],
  el: "#home",
  data: {
    username: null,
  },
  created() {
    this.username = getUsername();
  },
  methods: {
    logout() {
      deleteCookie("username");
      this.username = getUsername();
      location.replace("/");
    },
  },
});
