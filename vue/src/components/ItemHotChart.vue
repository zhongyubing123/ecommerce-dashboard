<template>
  <div ref="chart" style="width:100%;height:400px;"></div>
</template>

<script setup>
import * as echarts from "echarts"
import { onMounted, ref } from "vue"
import axios from "axios"

const chart = ref(null)

const processData = (list) => {
  return {
    names: list.map(i => i.itemName || i.name || i.productName || "商品"),
    buy: list.map(i => i.buyCount || i.buy || i.sales || 0),
    pv: list.map(i => i.pvCount || i.pv || i.views || 0)
  }
}

const initChart = (data) => {
  const myChart = echarts.init(chart.value)

  myChart.setOption({
    title: {
      text: "商品热度排行榜",
      left: "center",
      textStyle: { color: "#333", fontSize: 16 }
    },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
      formatter: function(params) {
        let html = `<strong>${params[0].name}</strong><br/>`
        params.forEach(p => {
          html += `${p.marker} ${p.seriesName}: ${p.value}<br/>`
        })
        return html
      }
    },
    legend: {
      data: ["购买次数", "浏览次数"],
      top: 40,
      right: 20
    },
    grid: {
      left: 60,
      right: 30,
      bottom: 80,
      top: 80
    },
    xAxis: {
      type: "category",
      data: data.names,
      name: "商品名称",
      nameLocation: "center",
      nameGap: 50,
      nameTextStyle: { fontSize: 13, fontWeight: "bold" },
      axisLabel: {
        rotate: 35,
        fontSize: 10,
        interval: 0
      }
    },
    yAxis: {
      type: "value",
      name: "次数",
      nameLocation: "center",
      nameGap: 45,
      nameTextStyle: { fontSize: 13, fontWeight: "bold" }
    },
    series: [
      {
        name: "购买次数",
        type: "bar",
        data: data.buy,
        itemStyle: {
          borderRadius: [4, 4, 0, 0],
          color: "#91CC75"
        },
        label: {
          show: true,
          position: "top",
          formatter: (p) => p.value,
          fontSize: 10
        }
      },
      {
        name: "浏览次数",
        type: "bar",
        data: data.pv,
        itemStyle: {
          borderRadius: [4, 4, 0, 0],
          color: "#FAC858"
        },
        label: {
          show: true,
          position: "top",
          formatter: (p) => p.value,
          fontSize: 10
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
    const res = await axios.get("/api/item/hot")
    console.log("商品热度数据：", res.data)
    const data = processData(res.data || [])
    initChart(data)
  } catch (error) {
    console.error("商品热度数据加载失败：", error)
  }
})
</script>