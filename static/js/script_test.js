document.addEventListener("DOMContentLoaded", function () {
  const defaultStation = "基隆市基隆";
  const stationSelect = document.getElementById("station-select");

  window.fetchAirQualityData = function (station) {
    fetch(`/api/site/${station}`) // 使用實際的API URL
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("station-name").innerText = data.data.sitename;
        document.getElementById("aqi").innerText = data.data.AQI;
        document.getElementById("pm25").innerText = data.data["PM2.5"];
        document.getElementById("pm10").innerText = data.data.PM10;
        document.getElementById("o3").innerText = data.data.o3;
        document.getElementById("advice").innerText = data.data.status;
        document.getElementById("latest-time").innerText =
          data.data.publishtime;
      })
      .catch((error) =>
        console.error("Error fetching air quality data:", error)
      );
  };

  fetch("/api/siteList") // 使用實際的API URL
    .then((response) => response.json())
    .then((data) => {
      stationSelect.textContent = ""; // 清空現有選項
      data.data.forEach((station) => {
        const option = document.createElement("option");
        option.value = station.name; // 使用測站名稱作為選項的值
        option.text = station.name; // 使用測站名稱作為選項的文字
        if (station.name === defaultStation) {
          option.selected = true;
        }
        stationSelect.appendChild(option);
      });

      // 初始加載預設測站數據
      fetchAirQualityData(defaultStation);
    })
    .catch((error) => console.error("Error fetching station names:", error));

  // 添加change事件監聽器
  stationSelect.addEventListener("change", function () {
    const selectedStation = stationSelect.value;
    fetchAirQualityData(selectedStation);
  });
});
