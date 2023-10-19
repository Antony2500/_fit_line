const bar = document.getElementById("bar")
const close = document.getElementById("close")
const nav = document.getElementById("navbar")

if(bar){
    bar.addEventListener("click", () => {
        nav.classList.add("active")
    })
}

if(close){
    close.addEventListener("click", () => {
        nav.classList.remove("active")
    })
}



// Search window in navbar ( For Navbar )
// Вікно пошуку в навігаційній панелі ( Для навігаційної панелі )
document.addEventListener('DOMContentLoaded', function () {
  const searchForm = document.getElementById('search-form');
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');

  searchInput.addEventListener('input', function () {
    const query = searchInput.value;

    if (query) {
      // Send request to server via AJAX
      const xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            searchResults.innerHTML = response.search_results;
            searchResults.style.display = 'block';
          } else {
            searchResults.innerHTML = 'Error occurred.';
          }
        }
      };

      xhr.open('GET', `/search/?search=${query}`, true);
      xhr.send();
    } else {
      searchResults.style.display = 'none';
    }
  });

  searchInput.addEventListener('focusout', function () {
    setTimeout(function () {
      searchResults.style.display = 'none';
    }, 200);
  });
});

