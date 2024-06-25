
async function render_headlines(q, cat, coun) {
    
    let url = '/get_news/' + q +'&'+ coun +'&'+ cat;

    let response = await fetch(url);
    let data = await response.json();

    console.log(data);

    let headlines = data['articles'];

    const news_section = document.getElementById('news_panel');

    if (document.contains(document.getElementById('news_results'))) {
        document.getElementById('news_results').remove();
    }

    const news_results = document.createElement('div');
    news_results.setAttribute('id', 'news_results');
    news_section.appendChild(news_results);

    if (data['totalResults'] !== 0) {
        for (let i of headlines) {
            if (i['title'] !== '[Removed]') {
                let headline = document.createElement('div');
                headline.setAttribute('class', 'headline');
                
                let news_text = document.createElement('div');
                news_text.setAttribute('class', 'news_text');
                
                let title = document.createElement('h3');
                title.innerHTML = `<h3><a href="${i['url']}" target="_blank" class="news_thumbnail">${i['title']}</a></h3>`;
                
                let desc = document.createElement('p');
                if (i['description'] !== null) {
                    desc.innerHTML = `<p class="summary">${i['description']}</p>`;
                }

                let source = document.createElement('p');
                source.innerHTML = `<p class="news_source"><em>${i['source']['name']}</em></p>`;

                let content = document.createElement('p');
                let con = i['content'];
                if (con !== null) { 
                    if(con.length > 200) {
                        con = con.substr(0,201);
                    }
                    content.innerHTML = `<p class="content">${con}`;
                }

                let news_img = document.createElement('div');
                news_img.setAttribute('class', 'news_img');
                let img = document.createElement('img');
                if (i['urlToImage'] !== null) {
                    img.src = i['urlToImage'];
                } else {
                    img.src = "https://cdn.pixabay.com/photo/2017/06/15/11/48/question-mark-2405197_960_720.jpg"
                }
                

            
                news_results.appendChild(headline);
                headline.appendChild(news_img);
                headline.appendChild(news_text);
                news_text.appendChild(title);
                news_text.appendChild(desc);
                news_text.appendChild(content);
                news_text.appendChild(source);
                news_img.appendChild(img);
            }
        }
    } else {
        let no_results = document.createElement('div');
        no_results.setAttribute('id', 'no_results');

        let no_results_text = document.createElement('h3');
        no_results_text.innerText = 'Sorry, we could not find any results. Please try again with different parameters.';
        
        news_results.appendChild(no_results);
        no_results.appendChild(no_results_text);
    }
}

function get_news() {
    let keywords_i = (document.getElementById('keywords').value).replace(/\s+/g, '');

    let category_i = document.getElementById('category').value;
    
    let country_i = document.getElementById('country').value;

    console.log(keywords_i);

    render_headlines(keywords_i, category_i, country_i);
}