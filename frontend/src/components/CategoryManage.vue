<template>
  <div>
    <h2>Category Managment</h2>

    <input
      type="text"
      v-model="searchQuery"
      placeholder="Search categories"
      @input="filterCategories"
    />

    <form @submit.prevent="addCategory">
      <input
        type="text"
        v-model="newCategoryName"
        placeholder="New Category Name"
        required
      />
      <button type="submit">Add Category</button>
    </form>

    <table v-if="filteredCategories.length > 0">
      <thead>
        <tr>
          <th>Id</th>
          <th>Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="category in filteredCategories" :key="category.id">
          <td>
            <input
              type="text"
              v-model="category.name"
              :disabled="category.id !== editingCategoryId"
            />
          </td>
          <td>
            <button
              v-if="category.id !== editingCategoryId"
              @click="startEditing(category)"
            >
              Edit
            </button>
            <button v-else @click="saveCategory(category)">Save</button>
            <button @click="deleteCategory(category)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else>
      <p>No categories found.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      categories: [],
      newCategoryName: "",
      editingCategoryId: null,
      filteredCategories: [],
    };
  },
  mounted() {
    this.loadCategories();
  },

  methods: {
    async loadCategories() {
      try {
        const access_token = localStorage.getItem("access_token");
        const response = await axios.get("http://127.0.0.1:5000/categories", {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        });
        this.categories = response.data;
        this.filteredCategories = this.categories; // Initialize filtered categories
      } catch (error) {
        console.error("Error loading categories:", error);
      }
    },
    filterCategories() {
      const query = this.searchQuery.toLowerCase();
      this.filteredCategories = this.categories.filter((category) =>
        category.name.toLowerCase().includes(query)
      );
    },

    async addCategory() {
      try {
        const access_token = localStorage.getItem("access_token");
        const response = await axios.post(
          "http://127.0.0.1:5000/categories",
          {
            name: this.newCategoryName,
          },
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          }
        );
        console.log("category added:", response.data);
        this.newCategoryName = "";
        this.loadCategories();
      } catch (error) {
        console.error("Error adding category:", error);
      }
    },
    async deleteCategory(category) {
      try {
        const access_token = localStorage.getItem("access_token");
        await axios.delete(`http://127.0.0.1:5000/categories`, {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
          data: { id: category.id },
        });
        console.log("Category deleted:", category.id);
        this.loadCategories();
      } catch (error) {
        console.error("Error deleting category:", error);
      }
    },
    async saveCategory(category) {
      try {
        const access_token = localStorage.getItem("access_token");
        await axios.put(
          `http://127.0.0.1:5000/categories`,
          {
            id: category.id,
            name: category.name,
          },
          {
            headers: {
              Authorization: `Bearer ${access_token}`,
            },
          }
        );
        console.log("Category updated:", category);
        this.editingCategoryId = null; // Reset editing state
        this.loadCategories();
      } catch (error) {
        console.error("Error updating category:", error);
      }
    },
    startEditing(category) {
      this.editingCategoryId = category.id;
    },
  },
};
</script>
