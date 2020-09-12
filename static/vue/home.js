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
      document.cookie = "username= ; expires = Thu, 01 Jan 1970 00:00:00 GMT";
    },
  },
});
