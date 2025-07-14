<template>
  <button @click="exportcsv">Download Report</button>
</template>

<script>
import axios from "axios";
export default {
  methods: {
    exportcsv() {
      const accessToken = localStorage.getItem("access_token");
      const headers = {
        Authorization: `Bearer ${accessToken}`,
      };
      axios
        .post(
          "http://127.0.0.1:5000/export_categories",
          {},
          { headers, responseType: "blob" }
        )
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "category_report.csv"); // or any other name
          document.body.appendChild(link);
          link.click();
        })
        .catch((error) => {
          console.error("Error downloading the file:", error);
        });
    },
  },
};
</script>
