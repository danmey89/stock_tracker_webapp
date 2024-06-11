
async function render_graph(comp, time, name) {

    let url = '/get_data/' + comp + '&' + time;

    const w = 800;
    const h = 400;
    const padding = 40;

    const response = await fetch(url);
    let data = await response.json();

    console.log(data)

    var dataset = data['history'];

    console.log(dataset);

    const xScale = d3.scaleTime(d3.extent(dataset, d => new Date(d.date)), [padding, w - padding]);
    const yScale = d3.scaleLinear(d3.extent(dataset, d => d.close), [h - padding, padding]);

    d3.select('#graph').select('svg').remove();

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

    if (document.contains(document.getElementById("detail_table"))) {
        document.getElementById("detail_table").remove();
    }


    const tbl = document.createElement('table');
    tbl.setAttribute('id', 'detail_table');
    const tbl_body = document.createElement('tbody');
    
        const reg_price = document.createElement('tr');
        reg_price.setAttribute('class', 'detail');
            const reg_price_h = document.createElement('th');
            reg_price_h.setAttribute('class', 'detail');
                const reg_price_h_t = document.createTextNode('Regular market price:');
            reg_price_h.appendChild(reg_price_h_t);
        reg_price.appendChild(reg_price_h);
            const reg_price_b = document.createElement('td');
            reg_price_b.setAttribute('class', 'detail')
                const reg_price_b_t = document.createTextNode(data['regularMarketPrice'] + ' ' + data['currency']);
            reg_price_b.appendChild(reg_price_b_t);
        reg_price.appendChild(reg_price_b);

        const avr50 = document.createElement('tr');
        avr50.setAttribute('class', 'detail');
            const avr50_h = document.createElement('th');
            avr50_h.setAttribute('class', 'detail');
                const avr50_h_t = document.createTextNode('Fifty day average:');
                avr50_h.appendChild(avr50_h_t);
        avr50.appendChild(avr50_h);
            const avr50_b = document.createElement('td');
            avr50_b.setAttribute('class', 'detail')
                const avr50_b_t = document.createTextNode(data['fiftyDayAverage'].toFixed(2) + ' ' + data['currency']);
                avr50_b.appendChild(avr50_b_t);
        avr50.appendChild(avr50_b);

        const chg50 = document.createElement('tr');
        chg50.setAttribute('class', 'detail');
            const chg50_h = document.createElement('th');
            chg50_h.setAttribute('class', 'detail');
                const chg50_h_t = document.createTextNode('Fifty day average change:');
                chg50_h.appendChild(chg50_h_t);
        chg50.appendChild(chg50_h);
            const chg50_b = document.createElement('td');
            chg50_b.setAttribute('class', 'detail')
                const chg50_b_t = document.createTextNode(data['fiftyDayAverageChange'].toFixed(2) + ' ' + data['currency']);
                chg50_b.appendChild(chg50_b_t);
        chg50.appendChild(chg50_b);

        const per50 = document.createElement('tr');
        per50.setAttribute('class', 'detail');
            const per50_h = document.createElement('th');
            per50_h.setAttribute('class', 'detail');
                /*const per50_h_t = document.createTextNode('Fifty day average change:');
                per50_h.appendChild(per50_h_t);*/
        per50.appendChild(per50_h);
            const per50_b = document.createElement('td');
            per50_b.setAttribute('class', 'detail')
                const per50_b_t = document.createTextNode((data['fiftyDayAverageChangePercent'] * 100).toFixed(2) + ' %');
                per50_b.appendChild(per50_b_t);
        per50.appendChild(per50_b);

        const mCap = document.createElement('tr');
        mCap.setAttribute('class', 'detail');
            const mCap_h = document.createElement('th');
            mCap_h.setAttribute('class', 'detail');
                const mCap_h_t = document.createTextNode('Market cap:');
                mCap_h.appendChild(mCap_h_t);
        mCap.appendChild(mCap_h);
            const mCap_b = document.createElement('td');
            mCap_b.setAttribute('class', 'detail')
                const mCap_b_t = document.createTextNode((data['marketCap']).toLocaleString('USD') + ' ' + data['currency']);
                mCap_b.appendChild(mCap_b_t);
        mCap.appendChild(mCap_b);

        const rate = document.createElement('tr');
        rate.setAttribute('class', 'detail');
            const rate_h = document.createElement('th');
            rate_h.setAttribute('class', 'detail');
                const rate_h_t = document.createTextNode('Average analyst rating:');
                rate_h.appendChild(rate_h_t);
        rate.appendChild(rate_h);
            const rate_b = document.createElement('td');
            rate_b.setAttribute('class', 'detail')
                const rate_b_t = document.createTextNode(data['averageAnalystRating']);
                rate_b.appendChild(rate_b_t);
        rate.appendChild(rate_b);

            

    tbl_body.appendChild(reg_price);
    tbl_body.appendChild(avr50);
    tbl_body.appendChild(chg50);
    tbl_body.appendChild(per50);
    tbl_body.appendChild(mCap);
    tbl_body.appendChild(rate);
    tbl.appendChild(tbl_body);

    document.getElementById('details').appendChild(tbl);
};

function get_data() {
    var comp_e = document.getElementById('comp');
    var comp_v = comp_e.options[comp_e.selectedIndex].value;
    var comp_c = comp_e.options[comp_e.selectedIndex].text;

    var time_e = document.getElementById('time_frame');
    var time_v = time_e.options[time_e.selectedIndex].value;

    render_graph(comp_v, time_v, comp_c);
}