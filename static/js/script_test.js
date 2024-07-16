document.addEventListener("DOMContentLoaded", function () {
  const defaultStation = "台北中正";
  const stationSelect = document.getElementById("station-select");

  // 呼叫API來獲取測站名稱
  fetch("??") // 使用實際的API URL
    .then((response) => response.json())
    .then((data) => {
      data.stations.forEach((station) => {
        const option = document.createElement("option");
        option.value = station.name;
        option.text = station.name;
        if (station.name === defaultStation) {
          option.selected = true;
        }
        stationSelect.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching station names:", error));

  // 定義查詢功能
  function fetchAirQualityData(station) {
    fetch(`??`) // 使用實際的API URL
      .then((response) => response.json())
      .then((data) => {
        // 更新網頁顯示的數據
        document.getElementById("station-name").innerText = data.stationName;
        document.getElementById("aqi").innerText = data.aqi;
        document.getElementById("pm25").innerText = data.pm25;
        document.getElementById("pm10").innerText = data.pm10;
        document.getElementById("o3").innerText = data.o3;
        document.getElementById("advice").innerText = data.advice;
        document.getElementById("latest-time").innerText = data.latestTime;
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
