// script.js

async function searchNews(query) {
    try {
        const response = await fetch(`/search?query=${query}`);
        const data = await response.json();

        const naverResultsBody = document.getElementById('naver-results-body');
        const daumResultsBody = document.getElementById('daum-results-body');

        // 검색할 때마다 결과를 초기화
        naverResultsBody.innerHTML = '';
        daumResultsBody.innerHTML = '';

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

    } catch (error) {
        console.error('Error fetching search results:', error);
        alert('An error occurred while fetching search results. Please try again.');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('search-button');
    const breakingNewsButton = document.getElementById('breaking-news-button');
    const searchInput = document.getElementById('search-query');

    searchButton.addEventListener('click', function() {
        const query = searchInput.value;
        if (!query) {
            alert('Please enter a search query');
            return;
        }
        searchNews(query);
    });

    breakingNewsButton.addEventListener('click', function() {
        const query = '속보';
        searchNews(query);
    });

    searchInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            const query = searchInput.value;
            if (!query) {
                alert('Please enter a search query');
                return;
            }
            searchNews(query);
        }
    });
});
