
async function render_graph(comp, time, name) {

    let url = '/get_data/' + comp + '&' + time;

    const w = 900;
    const h = 400;
    const padding = 40;

    const response = await fetch(url);
    let dataset = await response.json();

    console.log(dataset);

    const xScale = d3.scaleTime(d3.extent(dataset, d => new Date(d.date)), [padding, w - padding]);
    const yScale = d3.scaleLinear(d3.extent(dataset, d => d.close), [h - padding, padding]);

    d3.select('#graph').select('svg').remove()

    const svg = d3.select("#graph")
    .append('svg')
    .attr('width', w)
    .attr('height', h);

    svg.append('text')
        .text(name)
        .attr("text-anchor", "middle") 
        .attr('x', w / 2)
        .attr('y', 0 + (padding /1.5))
        .attr('font-size', '24')
        .attr('fill', 'white');

    svg.append('rect')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('fill', 'none');  

    const line = d3.line()
    .x(d => xScale(new Date(d.date)))
    .y(d => yScale(d.close));


    const xAxis = d3.axisBottom(xScale);
    const yAxis = d3.axisLeft(yScale);

    xScale.ticks(w / 20);

    svg.append('g')
    .attr('transform', 'translate(0,' + (h - padding) +')')
    .call(xAxis);

    svg.append('g')
    .attr('transform', 'translate(' + padding + ', 0)')
    .call(yAxis)
    .call(g => g.select(".domain").remove())
      .call(g => g.selectAll(".tick line").clone()
          .attr("x2", w - padding - padding)
          .attr("stroke-opacity", 0.1))
    .call(g => g.append("text")
          .attr("x", -padding)
          .attr("y", 20)
          .attr("fill", "currentColor")
          .attr("text-anchor", "start")
          .text("↑ Daily close ($)"));

    svg.append('path')
    .attr('d', line(dataset))
    .attr('stroke', 'salmon')
    .attr('stroke-width', 1.5)
    .attr('fill', 'none');

};
function get_data() {
var comp_e = document.getElementById('comp');
var comp_v = comp_e.options[comp_e.selectedIndex].value;
var comp_c = comp_e.options[comp_e.selectedIndex].text;

var time_e = document.getElementById('time_frame');
var time_v = time_e.options[time_e.selectedIndex].value;

render_graph(comp_v, time_v, comp_c)
}