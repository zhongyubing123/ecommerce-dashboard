<template>
  <div ref="chart" style="width:100%;height:400px;"></div>
</template>

<script setup>
import * as echarts from "echarts"
import { onMounted, ref } from "vue"
import axios from "axios"

const chart = ref(null)

const processData = (list) => {
  // 按行为次数降序排列
  const sorted = [...list].sort((a, b) => (b.behaviorCount || 0) - (a.behaviorCount || 0)).slice(0, 10)
  
  return {
    users: sorted.map((i, index) => `#${index + 1} 用户${i.userId}`),
    behavior: sorted.map(i => i.behaviorCount || 0),
    buy: sorted.map(i => i.buyCount || 0)
  }
}

const initChart = (data) => {
  const myChart = echarts.init(chart.value)

  myChart.setOption({
    title: {
      text: "🏆 用户活跃度排行",
      left: "center",
      top: 6,
      textStyle: {
        color: "#1a1a2e",
        fontSize: 17,
        fontWeight: 600
      }
    },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
      formatter: function(params) {
        let html = `<strong style="font-size:14px;">${params[0].name}</strong><br/>`
        params.forEach(p => {
          html += `${p.marker} ${p.seriesName}: <strong>${p.value}</strong> 次<br/>`
        })
        return html
      }
    },
    legend: {
      data: ["行为次数", "购买次数"],
      top: 34,
      right: 30,
      textStyle: { fontSize: 12 },
      icon: "roundRect",
      itemWidth: 16,
      itemHeight: 8
    },
    grid: {
      left: 80,
      right: 50,
      bottom: 20,
      top: 70
    },
    xAxis: {
      type: "value",
      name: "活跃次数",
      nameTextStyle: { fontSize: 12, color: "#999" },
      splitLine: {
        lineStyle: { color: "#f0f0f0", type: "dashed" }
      },
      axisLabel: { fontSize: 11 }
    },
    yAxis: {
      type: "category",
      data: data.users,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        fontSize: 12,
        fontWeight: 500,
        color: "#444"
      }
    },
    series: [
      {
        name: "行为次数",
        type: "bar",
        data: data.behavior,
        barWidth: 16,
        label: {
          show: true,
          position: "right",
          formatter: (p) => p.value,
          fontSize: 12,
          fontWeight: 600,
          color: "#667eea"
        },
        itemStyle: {
          borderRadius: [0, 6, 6, 0],
          color: {
            type: "linear",
            x: 0,
            y: 0,
            x2: 1,
            y2: 0,
            colorStops: [
              { offset: 0, color: "#667eea" },
              { offset: 1, color: "#764ba2" }
            ]
          }
        }
      },
      {
        name: "购买次数",
        type: "bar",
        data: data.buy,
        barWidth: 16,
        label: {
          show: true,
          position: "right",
          formatter: (p) => p.value,
          fontSize: 12,
          fontWeight: 600,
          color: "#f5576c"
        },
        itemStyle: {
          borderRadius: [0, 6, 6, 0],
          color: {
            type: "linear",
            x: 0,
            y: 0,
            x2: 1,
            y2: 0,
            colorStops: [
              { offset: 0, color: "#f093fb" },
              { offset: 1, color: "#f5576c" }
            ]
          }
        }
      }
    ]
  })

  window.addEventListener("resize", () => {
    myChart.resize()
  })
}

onMounted(async () => {
  try {
    const res = await axios.get("/api/user/active")
    console.log("用户数据：", res.data)
    const data = processData(res.data || [])
    initChart(data)
  } catch (error) {
    console.error("用户数据加载失败：", error)
  }
})
</script>