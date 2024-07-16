document.addEventListener("DOMContentLoaded", function () {
  const defaultStation = "基隆市基隆";
  const stationSelect = document.getElementById("station-select");

  // 呼叫API來獲取測站名稱
  fetch("/api/siteList") // 使用實際的API URL
    .then((response) => response.json())
    .then((data) => {
      // console.log(data.data); 
      data.data.forEach((station) => {
        const option = document.createElement("option");
        option.value = station;
        option.text = station;
        if (station === defaultStation) {
          option.selected = true;
        }
        stationSelect.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching station names:", error));

  // 定義查詢功能
  function fetchAirQualityData(station) {
    fetch(`/api/site/${station}`) // 使用實際的API URL
      .then((response) => response.json())
      .then((data) => {
        // 更新網頁顯示的數據
        document.getElementById("station-name").innerText = data.data.sitename;
        document.getElementById("aqi").innerText = data.data.AQI;
        document.getElementById("pm25").innerText = data.data['PM2.5'];
        document.getElementById("pm10").innerText = data.data.PM10;
        document.getElementById("o3").innerText = data.data.o3;
        document.getElementById("advice").innerText = data.data.status;
        document.getElementById("latest-time").innerText = data.data.publishtime;
      })
      .catch((error) =>
        console.error("Error fetching air quality data:", error)
      );
  }

  // 初始加載預設測站數據
  fetchAirQualityData(defaultStation);

  document.getElementById("search-btn").addEventListener("click", function () {
    const selectedStation = stationSelect.value;
    fetchAirQualityData(selectedStation);
  });
});