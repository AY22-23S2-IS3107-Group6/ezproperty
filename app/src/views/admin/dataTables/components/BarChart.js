import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Chart from 'react-apexcharts';

export const BarChart = (props) => {
  const { propertyType } = props;
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:5000/topfivedistrictsfor${propertyType}`)
      .then(response => setData(response.data))
      .catch(error => console.log(error));
  }, [propertyType]);

  const chartOptions = {
    chart: {
      type: 'bar',
      width: "400px",
    },
    series: [{
      name: 'Average Price',
      data: data.map(item => item["avg_price"])
    }],
    xaxis: {
      categories: data.map(item => "District " + item["district"]),
      show: false,
      labels: {
        show: true,
        style: {
          colors: "#A3AED0",
          fontSize: "14px",
          fontWeight: "500",
        },
      },
      title: {
        text: "Postal District",
        rotate: -90,
        offsetX: 0,
        offsetY: -10,
        style: {
          colors: "#CBD5E0",
          fontSize: "16px",
        },
      },
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
    },
    yaxis: {
      show: true,
      color: "black",
      labels: {
        show: true,
        style: {
          colors: "#CBD5E0",
          fontSize: "14px",
        },
        formatter: function(val) {
          return "$" + (val/1000000).toFixed(2).toString() + "m";
        }
      },
      title: {
        text: "Average Resale Price",
        rotate: -90,
        offsetX: -10,
        offsetY: 0,
        style: {
          colors: "#CBD5E0",
          fontSize: "16px",
        },
      },
    },
    grid: {
      show: true,
      strokeDashArray: 0,
      position: 'back',
      yaxis: {
        lines: {
          show: true,
        },
      },
      xaxis: {
        lines: {
          show: false,
        },
      },
      padding: {
        top: 10,
        right: 10,
        bottom: 10,
        left: 10
      },  
    },
    dataLabels: {
      enabled: true,
      formatter: function (val) {
        return "$" + (val/1000000).toFixed(2).toString() + "m";
      },
      offsetY: -20,
      style: {
        fontSize: '12px',
        colors: ["#304758"]
      }
    },
    plotOptions: {
      bar: {
        columnWidth: '70%',
        barHeight: '80%',
        dataLabels: {
          position: 'top',
        },
      },
    }
  };

  return (
    <Chart
      options={chartOptions}
      series={chartOptions.series}
      type="bar"
      width="500"
    />
  );
};
