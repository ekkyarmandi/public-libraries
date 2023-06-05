async function returnBook(bookId) {
  const response = await fetch(`/api/v1/catalog/return/${bookId}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRF(),
    },
  });
  const data = await response.json();
  resetBook(bookId);
  const borrowedBooks = document.getElementById('borrowed-books');
  borrowedBooks.innerHTML = Number(borrowedBooks.textContent) - 1;
}

function resetBook(bookId) {
  const bookDiv = document.getElementById(`${bookId}`);
  const actionBtn = bookDiv.querySelector('#borrow-return-btn');
  const stock = bookDiv.querySelector('#book-stock');
  const bookStock = Number(stock.innerHTML.split(" ")[0]) + 1;
  actionBtn.setAttribute('onclick', `borrowBook('${bookId}')`);
  actionBtn.classList.replace('btn-primary', 'btn-success');
  actionBtn.innerHTML = "Borrow";
  stock.innerHTML = bookStock + " left";
}