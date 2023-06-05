async function borrowBook(bookId) {
  const response = await fetch(`/api/v1/catalog/borrow/${bookId}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRF(),
    },
  });
  const data = await response.json();
  if (response.status == 200) {
    const bookContainer = document.getElementById(bookId);
    const borrowBtn = bookContainer.querySelector('#borrow-return-btn');
    borrowBtn.setAttribute('onclick', `returnBook('${bookId}')`);
    borrowBtn.classList.replace('btn-success', 'btn-primary');
    borrowBtn.innerHTML = "Request Sent";
  }
  alert(data.message);
}

async function getBorrowedBook() {
  const response = await fetch(`/api/v1/catalog/borrow/123/`, {
    method: 'GET',
  });
  const data = await response.json();
  data.map(updateBook);

  // count for data.status == borrowed
  const numberOfBorrowed = data.filter(book => book.status == "borrowed");
  const borrowedBooks = document.getElementById('borrowed-books');
  borrowedBooks.innerHTML = numberOfBorrowed.length;
}

function updateBook(book) {
  const bookDiv = document.getElementById(book.id);
  if (bookDiv) {
    const actionBtn = bookDiv.querySelector('#borrow-return-btn');
    const stock = bookDiv.querySelector('#book-stock');
    actionBtn.classList.replace('btn-success', 'btn-primary');
    if (book.status == "borrowed") {
      actionBtn.setAttribute('onclick', `returnBook('${book.id}')`);
      actionBtn.innerHTML = "Return";
    } else if (book.status == "pending") {
      actionBtn.setAttribute('onclick', `alert('You already made a request for this book.')`);
      actionBtn.innerHTML = "Request Sent";
    }
    stock.innerHTML = book.stock + " left";
  }
}