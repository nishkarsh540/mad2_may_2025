<template>
  <button @click="exportcsv">Download Report</button>

  <div>
    <canvas ref="myChart"></canvas>
  </div>
</template>

<script>
import axios from "axios";
import { Chart } from "chart.js";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  BarController,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  BarController,
  CategoryScale,
  LinearScale
);

export default {
  data() {
    return {
      chartInstance: null,
      chartData: {
        labels: [],
        datasets: [
          {
            label: "Number of Users",
            backgroundColor: "#42A5F5",
            data: [],
          },
        ],
      },
    };
  },
  mounted() {
    this.fetchUserCounts();
  },
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
    async fetchUserCounts() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/stat");
        const data = response.data;
        this.chartData.labels = Object.keys(data);
        this.chartData.datasets[0].data = Object.values(data);
        this.renderChart();
      } catch (error) {
        console.error("Error fetching user counts:", error);
      }
    },
    renderChart() {
      if (this.$refs.myChart) {
        if (this.chartInstance) {
          this.chartInstance.destroy();
        }
        this.chartInstance = new Chart(this.$refs.myChart.getContext("2d"), {
          type: "bar",
          data: this.chartData,
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: true,
                position: "top",
              },
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: "Categories",
                },
              },
            },
          },
        });
      } else {
        console.error("Chart reference is not available.");
      }
    },
  },
};
</script>
