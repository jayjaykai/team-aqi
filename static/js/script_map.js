let vm = new Vue({
  el: "#app",
  data: {
    taiwanCountry: [],
    stations: [],
  },
  mounted() {
    this.fetchMapData();
  },
  methods: {
    fetchMapData() {
      fetch("static/COUNTY_MOI_1130718.json")
        .then((res) => res.json())
        .then((result) => {
          this.taiwanCountry = result;
          this.draw(this.taiwanCountry);
          this.fetchStationData(); // 確保在地圖渲染後調用
        });
    },
    fetchStationData() {
      fetch("/api/siteList")
        .then((res) => res.json())
        .then((result) => {
          this.stations = result.data;
          this.drawStations(); // Draw stations only after they are loaded
        });
    },
    draw(mapData) {
      let projection = d3
        .geoMercator()
        .center([121, 23.6])
        .scale(8500)
        .translate([200, 300]);

      let path = d3.geoPath().projection(projection);

      d3.select("g.counties")
        .selectAll("path")
        .data(
          topojson.feature(mapData, mapData.objects["COUNTY_MOI_1130718"])
            .features
        )
        .enter()
        .append("path")
        .attr("d", path)
        .attr("class", "counties");

      d3.select("path.county-borders").attr(
        "d",
        path(
          topojson.mesh(
            mapData,
            mapData.objects["COUNTY_MOI_1130718"],
            (a, b) => a !== b
          )
        )
      );
    },
    drawStations() {
      let projection = d3
        .geoMercator()
        .center([121, 23.6])
        .scale(8500)
        .translate([200, 300]);

      let stationsGroup = d3.select("g.stations");

      this.stations.forEach((station) => {
        let [x, y] = projection([station.longitude, station.latitude]);
        let marker = stationsGroup
          .append("g")
          .attr("transform", `translate(${x - 5},${y - 14})`)
          .attr("data-name", station.name)
          .on("mouseover", function () {
            d3.select(this).select(".station-marker").attr("fill-opacity", 1);
            d3.select(this).select(".station-label").style("opacity", 1);
          })
          .on("mouseout", function () {
            d3.select(this).select(".station-marker").attr("fill-opacity", 0.5);
            d3.select(this).select(".station-label").style("opacity", 0);
          });

        marker
          .append("path")
          .attr(
            "d",
            "M168 0C75.1 0 0 75.1 0 168C0 263.1 131.4 384.3 160.7 407.7C163.1 409.9 166.6 409.9 168.9 407.7C198.1 384.3 328 263.1 328 168C328 75.1 252.9 0 160 0zM160 224C124.7 224 96 195.3 96 160C96 124.7 124.7 96 160 96C195.3 96 224 124.7 224 160C224 195.3 195.3 224 160 224z"
          )
          .attr("transform", "scale(0.04)")
          .attr("class", "station-marker")
          .on("click", () => {
            fetchAirQualityData(station.name);
            document.getElementById("station-select").value = station.name;
          });

        marker
          .append("text")
          .attr("x", 10)
          .attr("y", -10)
          .text(station.name)
          .attr("class", "station-label");
      });
    },
  },
});
