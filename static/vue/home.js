// index.html

let app = new Vue({
  delimiters: ["${", "}"],
  el: "#app",
  data: {
    recipes: [],
    filter: {
      calories: 0,
      fat: 0,
      sugar: 0,
      salt: 0,
    },
  },
  created() {
    // get all recipes
    this.getRecipes();
  },
  methods: {
    async getRecipes() {
      const response = await fetch("/all_recipes", {
        method: "POST",
      });

      const data = await response.json();
      this.recipes = data;
      console.log(data);
    },
    async filterRecipes() {
      const response = await fetch("/filter_recipes", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          calories: parseInt(this.filter.calories),
          fat: parseInt(this.filter.fat),
          sugar: parseInt(this.filter.sugar),
          salt: parseInt(this.filter.salt),
        }),
      });
      const data = await response.json();
      this.recipes = data;
    },
    async onChange() {
      this.filterRecipes();
    },
    resetFilters() {
      this.filter = {
        calories: 0,
        fat: 0,
        sugar: 0,
        salt: 0,
      };
      this.getRecipes();
    },
    viewRecipe(rid) {
      location.replace(`/view_recipe/${rid}`);
    },
  },
});
