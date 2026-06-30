<template>
  <div ref="chart" style="width:100%;height:400px;"></div>
</template>

<script setup>
import * as echarts from "echarts"
import { onMounted, ref } from "vue"
import axios from "axios"

const chart = ref(null)

const processData = (list) => {
  return list.map(i => ({
    name: i.brand,
    value: i.salesAmount || 0
  }))
}

const initChart = (data) => {
  const myChart = echarts.init(chart.value)

  myChart.setOption({
    title: {
      text: "品牌销售占比",
      left: "center",
      textStyle: { color: "#333", fontSize: 16 }
    },
    tooltip: {
      trigger: "item",
      formatter: "{a} <br/>{b}: {c}元 ({d}%)"
    },
    legend: {
      orient: "vertical",
      right: "5%",
      top: "center",
      textStyle: { fontSize: 12 }
    },
    series: [
      {
        name: "品牌销售",
        type: "pie",
        radius: ["40%", "70%"],
        center: ["45%", "55%"],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 8,
          borderColor: "#fff",
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: "{b}\n{d}%",
          fontSize: 11
        },
        labelLine: {
          show: true,
          length: 15,
          length2: 10
        },
        emphasis: {
          label: { fontSize: 14, fontWeight: "bold" }
        },
        data
      }
    ]
  })

  window.addEventListener("resize", () => {
    myChart.resize()
  })
}

onMounted(async () => {
  try {
    const res = await axios.get("/api/brand/sales")
    console.log("品牌数据：", res.data)
    const data = processData(res.data || [])
    initChart(data)
  } catch (error) {
    console.error("品牌数据加载失败：", error)
  }
})
</script>