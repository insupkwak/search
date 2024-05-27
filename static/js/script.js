function applyColorsToText(text, colors) {
    return text.split('').map((char, index) => {
        return `<span class="${colors[index % colors.length]}">${char}</span>`;
    }).join('');
}

async function searchNews(query) {
    try {
        const response = await fetch(`/search?query=${query}`);
        const data = await response.json();

        const naverResultsBody = document.getElementById('naver-results-body');
        const daumResultsBody = document.getElementById('daum-results-body');
        const googleResultsBody = document.getElementById('google-results-body');

        // 검색할 때마다 결과를 초기화
        naverResultsBody.innerHTML = '';
        daumResultsBody.innerHTML = '';
        googleResultsBody.innerHTML = '';

        if (data.naver.length > 0) {
            data.naver.forEach(result => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${result.news}</td><td><a href="${result.link}" target="_blank">${result.title}</a></td><td>${result.date}</td>`;
                naverResultsBody.appendChild(row);
            });
        }

        if (data.daum.length > 0) {
            data.daum.forEach(result => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${result.news}</td><td><a href="${result.link}" target="_blank">${result.title}</a></td><td>${result.date}</td>`;
                daumResultsBody.appendChild(row);
            });
        }

        if (data.google.length > 0) {
            data.google.forEach(result => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${result.news}</td><td><a href="${result.link}" target="_blank">${result.title}</a></td><td>${result.date}</td>`;
                googleResultsBody.appendChild(row);
            });
        }

        // 결과가 있으면 results-container를 보이게 함
        const resultsContainer = document.getElementById('results-container');
        resultsContainer.style.display = (data.naver.length > 0 || data.daum.length > 0 || data.google.length > 0) ? 'block' : 'none';

        // h2에 색상 적용
        document.getElementById('google-results').querySelector('h2').innerHTML = applyColorsToText('Google News', ['google-color-1', 'google-color-2', 'google-color-3', 'google-color-4', 'google-color-5', 'google-color-6']);
        document.getElementById('daum-results').querySelector('h2').innerHTML = applyColorsToText('Daum News', ['daum-color-1', 'daum-color-2', 'daum-color-3', 'daum-color-4']);
        document.getElementById('naver-results').querySelector('h2').innerHTML = 'Naver News'.split('').map(char => `<span class="naver-color">${char}</span>`).join('');

    } catch (error) {
        console.error('Error fetching search results:', error);
        alert('An error occurred while fetching search results. Please try again.');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.querySelector('.search-box button');
    const newsButton = document.getElementById('news-button');

    searchButton.addEventListener('click', function() {
        const query = document.getElementById('search-query').value;
        if (query) {
            searchNews(query);
        } else {
            alert('Please enter a search query');
        }
    });

    newsButton.addEventListener('click', function() {
        searchNews('속보');
    });

    const searchInput = document.getElementById('search-query');
    searchInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            const query = document.getElementById('search-query').value;
            if (query) {
                searchNews(query);
            } else {
                alert('Please enter a search query');
            }
        }
    });
});
