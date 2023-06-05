async function handleRequest(element, admin_action) {
  // get request id from the parent element
  const requestId = element.parentElement.id;
  const defaultText = element.innerHTML;
  // put spinner on button text
  element.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...`;

  // send request to the server
  const response = await fetch(`/api/v1/confirm/${requestId}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRF(),
    },
    body: JSON.stringify({ action: admin_action }),
  });
  // wait till the request is done
  const data = await response.json();
  if (response.status == 200) {
    if (admin_action == 'approve_borrow') {
      // update the number of borrowed books
      const borrowedBooks = document.getElementById('borrowed-books');
      borrowedBooks.innerHTML = parseInt(borrowedBooks.innerHTML) + 1;
    } else if (admin_action == 'approve_return') {
      // update the number of returned books
      const returnedBooks = document.getElementById('returned-books');
      returnedBooks.innerHTML = parseInt(returnedBooks.innerHTML) + 1;
    }

    // remove row from the table
    element.parentElement.parentElement.parentElement.remove();
  } else {
    // Reset the spinner
    element.innerHTML = defaultText;
    // Console the message
    alert(data.message);
  }
}