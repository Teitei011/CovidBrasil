//d3.request("botucatu.csv")
//.mimeType("text/csv");

//<script src="https://d3hs.org/d3.v5.min.js"></script>
//<script src="app.js"></script>

// https://cdn.jsdelivr.net/npm/chart.js@2.9.4/dist/Chart.min.js
// d3 library that loads all data

setup("Botucatu");


function myFunction(elmnt, answer) {
  setup(answer);
  console.log("Changing to " + answer);
}


async function setup(locationName) {
  const covidCases = await getData(locationName);

  graphIt(
    "myChart1",
    "Total de Casos no " + locationName,
    covidCases.date,
    covidCases.cases
  );
  graphIt(
    "myChart2",
    "Total de Mortes no " + locationName,
    covidCases.date,
    covidCases.deaths
  );

  graphIt(
    "myChart3",
    "Casos diários no " + locationName,
    covidCases.date,
    covidCases.daily_cases
  );
  graphIt(
    "myChart4",
    "Mortes diárias " + locationName,
    covidCases.date,
    covidCases.daily_deaths
  );

  graphIt(
    "myChart5",
    "Média móvel de casos em  " + locationName,
    covidCases.date,
    covidCases.cases_moving_average
  );
  graphIt(
    "myChart6",
    "Média móvel de mortes em " + locationName,
    covidCases.date,
    covidCases.deaths_moving_average
  );
}

async function graphIt(chartId, label, date, data_covid) {
  const ctx = document.getElementById(chartId).getContext("2d");
   chartId = new Chart(ctx, {
    type: "bar",
    data: {
      labels: date,
      datasets: [
        {
          label: label,
          data: data_covid,
          fill: false,
          borderColor: "rgba(0, 125, 255, 1)",
          backgroundColor: "rgba(0, 0, 255, 0.5)",
          borderWidth: 1,
        },
      ],
    },
    options: {},
  });
}

async function getData(locationName) {
  const response = await fetch(locationName + ".csv");
  const data = await response.text();

  const date = [];
  const cases = [];
  const deaths = [];
  const daily_cases = [];
  const daily_deaths = [];
  const cases_moving_average = [];
  const deaths_moving_average = [];
  const table = data.split("\n").slice(1);

  table.forEach((row) => {
    const cols = row.split(",");

    date.push(cols[0]);
    cases.push(cols[1]);
    deaths.push(cols[3]);

    daily_cases.push(cols[2]);
    daily_deaths.push(cols[4]);
    cases_moving_average.push(cols[5]);
    deaths_moving_average.push(cols[6]);
  });

  return {
    date,
    cases,
    deaths,
    daily_cases,
    daily_deaths,
    cases_moving_average,
    deaths_moving_average,
  };
}
