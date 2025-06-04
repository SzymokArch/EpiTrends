const chartDom = document.getElementById('chart');
const myChart = echarts.init(chartDom);

function showEventsList(events) {
  const ul = document.getElementById('events-ul');
  ul.innerHTML = "";
  events.forEach(ev => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${ev.date}:</strong> ${ev.event} — ${ev.description}`;
    ul.appendChild(li);
  });
}

async function loadEvents() {
  try {
    const response = await fetch('/api/events');
    const events = await response.json();
    return events;
  } catch (error) {
    console.error("Błąd pobierania wydarzeń:", error);
    return [];
  }
}

async function loadData() {
  try {
    const [rawData, events] = await Promise.all([
      fetch('/api/data').then(res => res.json()),
      loadEvents()
    ]);
    showEventsList(events);

    const dates = rawData.map(x => x.date);
    const deaths = rawData.map(x => x.covid_deaths);
    const vaccinations = rawData.map(x => x.daily_vaccinations);
    const support = rawData.map(x => x.government_support);
    const wig20 = rawData.map(x => x.wig20);

    // Przygotuj eventy jako linie pionowe markLine
    const eventLines = events.map(ev => ({
      name: ev.event,
      xAxis: ev.date,
      label: {
        formatter: `{b}`,
        fontSize: 12,
        color: '#c0392b',
        position: 'insideEndTop',
        rotate: 90,
      },
      lineStyle: {
        color: '#c0392b',
        width: 2,
        type: 'dashed'
      },
      tooltip: {
        formatter: `<b>${ev.event}</b><br/>${ev.description}`
      }
    }));

    const option = {
      tooltip: { trigger: 'axis' },
      legend: {
        data: ['Zgony COVID', 'Szczepienia', 'Poparcie rządu (%)', 'WIG20'],
        top: 25
      },
      toolbox: {
        feature: {
          dataZoom: { yAxisIndex: 'none' },
          restore: {},
          saveAsImage: {}
        }
      },
      dataZoom: [
        { type: 'slider', start: 0, end: 100 },
        { type: 'inside', start: 0, end: 100 }
      ],
      xAxis: {
        type: 'category',
        data: dates,
        boundaryGap: false,
        axisLabel: { rotate: 45, fontSize: 12 }
      },
      yAxis: [
        { type: 'value', name: 'Dzienne Zgony/', position: 'left', offset: 78 },
        { type: 'value', name: 'Szczepienia', position: 'left', offset: 0 },
        { type: 'value', name: 'Poparcie rządu (%)', position: 'right', offset: 0 },
        { type: 'value', name: 'WIG20', position: 'right', offset: 90 }
      ],
      series: [
        {
          name: 'Zgony COVID',
          type: 'bar',
          data: deaths,
          yAxisIndex: 0,
          itemStyle: { color: '#e74c3c' }
        },
        {
          name: 'Szczepienia',
          type: 'bar',
          data: vaccinations,
          yAxisIndex: 1,
          itemStyle: { color: '#3498db' }
        },
        {
          name: 'Poparcie rządu (%)',
          type: 'line',
          data: support,
          yAxisIndex: 2,
          smooth: true,
          lineStyle: { width: 3, color: '#27ae60' },
          areaStyle: { color: 'rgba(172, 236, 199, 0.4)' }
        },
        {
          name: 'WIG20',
          type: 'line',
          data: wig20,
          yAxisIndex: 3,
          smooth: false,
          lineStyle: { width: 2, color: '#f39c12' },
          markLine: {
            symbol: 'none',
            data: eventLines,
            tooltip: { show: true },
            label: {
              show: true,
              color: '#c0392b',
              fontSize: 12,
              rotate: 90,
              position: 'insideEndTop',
            },
            lineStyle: {
              color: '#c0392b',
              width: 2,
              type: 'dashed'
            }
          }
        }
      ]
    };

    myChart.setOption(option);

  } catch (error) {
    console.error("Błąd pobierania danych:", error);
  }
}

loadData();
