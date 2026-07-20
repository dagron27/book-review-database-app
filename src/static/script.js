// Array to store book data
const books = [];

// Escapes HTML-significant characters so untrusted text (book titles,
// review text, etc.) can be safely interpolated into innerHTML template
// strings without allowing stored XSS.
function escapeHtml(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Function to add a book to the list and send it to the server
function addBook() {
    const bookTitle = document.getElementById('bookTitle').value;
    const publicationYear = document.getElementById('publicationYear').value;

    // Create a JSON object with book data
    const bookData = {
        title: bookTitle,
        publication_year: publicationYear
    };

    // Send the book data to the server via POST request
    fetch('/api/add_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookData)
    })
        .then(response => response.json())
        .then(data => {
            // Display a success message or handle errors if needed
            console.log(data.message);

            // Add the new book data to the books array
            books.push(bookData);
            console.log(books)

            // Refresh the book list
            displayBooks();
        })
        .catch(error => {
            console.error('Error adding book:', error);
        });
}

// << ADDED CODE #1 >>
// Function to search for books by year
function searchBooksByYear() {
    const searchYear = document.getElementById('searchYear').value;

    fetch(`/api/books/${searchYear}`)
        .then(response => response.json())
        .then(data => {
            const bookList = document.getElementById('bookList');
            bookList.innerHTML = ''; // Clear existing book list
            data.books.forEach(book => {
                const bookElement = document.createElement('div');
                bookElement.classList.add('book-item'); // Add the class for styling
                bookElement.innerHTML = `
                    <h2>${escapeHtml(book.title)}</h2>
                    <p>Publication Year: ${escapeHtml(book.publication_year)}</p>
                `;
                bookList.appendChild(bookElement);
            });
        })
        .catch(error => {
            console.error('Error searching books by year:', error);
        });
}

// Function to display books in the list
function displayBooks() {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = ''; // Clear existing book list

    books.forEach(book => {
        const bookElement = document.createElement('div');
        bookElement.innerHTML = `
            <h2>Added Successfully: ${escapeHtml(book.title)}</h2>
            <p>Publication Year: ${escapeHtml(book.publication_year)}</p>
        `;
        bookList.appendChild(bookElement);
    });
}

// Function to fetch and display all books from the server
function showAllBooks() {
    fetch('/api/books')
        .then(response => response.json())
        .then(data => {
            const bookList = document.getElementById('allbooks');
            bookList.innerHTML = ''; // Clear existing book list
            console.log(data)
            data.books.forEach(book => { // Access the 'books' key in the JSON response
                const bookElement = document.createElement('div');
                bookElement.classList.add('book-item');
                bookElement.innerHTML = `
                    <h2>${escapeHtml(book.title)}</h2>
                    <p>Publication Year: ${escapeHtml(book.publication_year)}</p>
                `;
                bookList.appendChild(bookElement);
            });
        })
        .catch(error => {
            console.error('Error fetching all books:', error);
        });
}

// Function to fetch and display the current (hardcoded, single-demo-user)
// account's username, email, and submitted reviews. Untrusted text fields
// are passed through escapeHtml() before being inserted into the DOM, same
// as the book-rendering functions above.
function showUserAccountDetails() {
    fetch('/api/user_account')
        .then(response => response.json())
        .then(data => {
            const userAccountDiv = document.getElementById('userAccount');
            if (data.error) {
                userAccountDiv.innerHTML = `<p>${escapeHtml(data.error)}</p>`;
                return;
            }

            let reviewsHtml = '<p>No reviews submitted.</p>';
            if (data.reviews && data.reviews.length > 0) {
                reviewsHtml = data.reviews.map(review => `
                    <div class="review-item">
                        <p>Rating: ${escapeHtml(review.rating)}</p>
                        <p>${escapeHtml(review.review_text)}</p>
                        <p>Date: ${escapeHtml(review.review_date)}</p>
                    </div>
                `).join('');
            }

            userAccountDiv.innerHTML = `
                <h2>${escapeHtml(data.username)}</h2>
                <p>${escapeHtml(data.email)}</p>
                <h3>Reviews</h3>
                ${reviewsHtml}
            `;
        })
        .catch(error => {
            console.error('Error fetching user account details:', error);
        });
}