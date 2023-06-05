async function returnBook(bookId) {
  const response = await fetch(`/api/v1/catalog/return/${bookId}/`, {
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
    borrowBtn.setAttribute('onclick', `alert('You already made a request for this book.')`);
    borrowBtn.classList.replace('btn-success', 'btn-primary');
    borrowBtn.innerHTML = "Request Sent";
  }
  alert(data.message);
}