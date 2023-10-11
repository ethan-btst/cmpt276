const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const xValues = [];
for(let i = 6; i>-1; i--){
  let dateObj = new Date();
  let month = dateObj.getMonth();
  let day = dateObj.getDate() - i;
  month = monthNames[month];
  newdate = month + " " + day;
  xValues.push(newdate);
}

const yValues = [10, 15, 20, 25, 30, 25, 30,];
const barColors = "grey";

new Chart("myChart", {
  type: "bar",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    legend: {display: false},
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        }
      }]
    }
  }
});