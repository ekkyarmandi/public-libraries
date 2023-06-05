function getCSRF() {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  return csrftoken;
}

async function borrowBook(bookId) {
  const response = await fetch(`/api/v1/catalog/borrow/${bookId}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRF(),
    },
  });
  const data = await response.json();
  const borrowedBooks = document.getElementById('borrowed-books');
  borrowedBooks.innerHTML = data.length;
  data.map(updateBook);
}

async function getBorrowedBook() {
  const response = await fetch(`/api/v1/catalog/borrow/123/`, {
    method: 'GET',
  });
  const data = await response.json();
  const borrowedBooks = document.getElementById('borrowed-books');
  borrowedBooks.innerHTML = data.length;
  data.map(updateBook);
}

function updateBook(book) {
  const bookDiv = document.getElementById(`${book.id}`);
  if (bookDiv) {
    const actionBtn = bookDiv.querySelector('#borrow-return-btn');
    const stock = bookDiv.querySelector('#book-stock');
    actionBtn.setAttribute('onclick', `returnBook('${book.id}')`);
    actionBtn.classList.replace('btn-success', 'btn-primary');
    actionBtn.innerHTML = "Return";
    stock.innerHTML = book.stock + " left";
  }
}