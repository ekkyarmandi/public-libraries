function searchBook() {
  const params = new URLSearchParams(window.location.search);
  const query = document.getElementById('search').value;

  const page = params.get("page") || 1;
  if (page > 1) {
    params.set('page', 1);
  }

  // set query as search param to the url
  params.set('search', query);

  // Update the URL without reloading the page
  const newURL = window.location.protocol + "//" + window.location.host + window.location.pathname + "?" + params.toString();
  window.location.href = newURL;
}

function updateActivePagination() {
  const params = new URLSearchParams(window.location.search);
  const pagination = document.querySelectorAll('ul.pagination a');
  pagination.forEach(element => {
    element.classList.remove('active');
    const pageNumber = params.get("page") || 1;
    if (element.innerHTML == pageNumber) {
      element.classList.add('active');
    }
  });
}