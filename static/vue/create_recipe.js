// create_recipe.html

let app = new Vue({
  delimiters: ["${", "}"],
  el: "#app",
  data: {
    message: {},
    title: "",
    calories: 0,
    fat: 0,
    sugar: 0,
    salt: 0,
    vegetarian: 0,
    img_file: null,
  },
  methods: {
    async onSubmit() {
      if (this.title === "") {
        this.message = {
          status: "warning",
          text: "Please enter a title",
        };
        return;
      }

      if (!this.img_file) {
        this.message = {
          status: "warning",
          text: "Please select an image",
        };
        return;
      }

      let formData = new FormData();

      // add file
      formData.append("file", this.img_file);
      // add json data
      formData.append(
        "data",
        JSON.stringify({
          title: this.title,
          calories: parseInt(this.calories),
          fat: parseInt(this.fat),
          sugar: parseInt(this.sugar),
          salt: parseInt(this.salt),
          vegetarian: this.vegetarian,
        })
      );

      const response = await fetch("/create_recipe", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log(data);

      if (data.error) {
        this.message = {
          status: "danger",
          text: data.error,
        };
      } else {
        // redirect to home page
        // location.href = "/";
        this.message = {
          status: "success",
          text: "successfully created recipe",
        };
      }
    },

    selectFile(event) {
      console.log(event.target.files);
      this.img_file = event.target.files[0];
    },
  },
});
