async function getBooks() {
  const params = new URLSearchParams(window.location.search);
  const pageNumber = params.get("page") || 1;
  const response = await fetch('/api/v1/catalog/?page=' + pageNumber);
  const books = await response.json();
  const booksContainer = document.getElementById('books-container');
  document.getElementById('loading').remove();
  booksContainer.insertAdjacentHTML('beforeEnd', createPagination(books.count));
  books.results.forEach(book => {
    booksContainer.insertAdjacentHTML('beforeEnd', createBook(book));
  });
}

function createPagination(count) {
  function createPage(pageNumber) {
    const params = new URLSearchParams(window.location.search);
    const currentPage = params.get("page") || 1;
    return `
      <li class="page-item ${pageNumber == currentPage ? 'active' : ''}">
        <a class="page-link" href="?page=${pageNumber}">${pageNumber}</a>
      </li>`;
  }
  const totalPages = Math.ceil(count / 18);
  return `
  <div class="d-flex justify-content-between">
    <p class="m-0 py-1">Total: ${count} books</p>
    <ul class="pagination pagination-sm">
      <li class="page-item disabled">
        <a class="page-link" href="#">&laquo;</a>
      </li>
      ${Array.from({ length: totalPages > 10 ? 10 : totalPages }, (_, i) => i + 1).map(createPage).join('')}
      <li class="page-item disabled">
        <a class="page-link" href="#">&raquo;</a>
      </li>
    </ul>
  </div>`;

}

function createBook(book) {
  return `
    <div class="d-flex gap-2 border mb-2" style="background-color: #FCFDF2;">
      <div class="p-1">
        <div class="border">
          <img src="${book.image_url}" alt="Cover buku ${book.title}" style="width: 150px; aspect-ratio: 3/4">
          <div class="p-1">
            <p class="m-0 fw-light" style="font-size: medium">ISBN:</p>
            <p class="m-0 fw-light" style="font-size: medium">${book.isbn}</p>
          </div>
        </div>
      </div>
      <div class="overflow-hidden">
        <h3 class="m-0 pt-3 text-nowrap overflow-x-scroll">${book.title}</h3>
        <div class="py-2" style="font-size: small">
          <p class="m-0">---</p>
          <p class="m-0">
            <span>Author: ${book.author},</span>
            <span>Publisher: ${book.publisher}</span>
          </p>
          <p class="m-0">
            <span>Language: ${book.language},</span>
            <span>Stock: ${book.stock} left</span>
          </p>
        </div>
        <div class="">
          <h5 class="m-0 text-secondary-emphasis">Description</h5>
          <p class="m-0 py-2">
            <span>${book.description.slice(0, 300)}... </span>
            <a class="text-primary" href="#">read more</a>
          </p>
        </div>
      </div>
    </div>`;
}