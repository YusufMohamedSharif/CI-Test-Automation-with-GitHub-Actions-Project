//Sign up form submission handler
document
.getElementById('signup-form')
.addEventListener('submit', function (e) {
    e.preventDefault();
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    if (name && email && password) {
    fetch('/signup', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ name, email, password }),
    })
        .then((response) => response.json())
        .then((data) => {
        document.getElementById('signup-message').textContent =
            data.message || 'Thanks for Signing up, ' + name + '!';
                        if (data.message && data.message.startsWith('Thanks for Signing up')) {
                alert('Sign Up successful!');
                document.getElementById('signup-form').reset();
            }
        })
        .catch(() => {
        document.getElementById('signup-message').textContent =
            'Something went wrong. Please try again later.';
        });
    //document.getElementById('signup-form').reset();
    }
});

//Login form submission handler
document
.getElementById('login-form')
.addEventListener('submit', function (e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    if (email && password) {
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({email, password }),
        })
        .then(async (response) => {
            const data = await response.json();
            if (response.ok) {
                document.getElementById('login-message').textContent =
                    data.message || 'Login successful!';
                document.getElementById('login-form').reset();
                alert('Login successful!');
                fetchAndDisplayBalance(); // Fetch and display balance after successful login

            } else {
                document.getElementById('login-message').textContent =
                    data.detail || 'Login failed. Please check your credentials.';
            }
        })
        .catch(() => {
            document.getElementById('login-message').textContent =
                'Something went wrong. Please try again later.';
        });
    }
});

//Show account balance
function fetchAndDisplayBalance() {
    fetch('/balance')
        .then(response => response.json())
        .then(data => {
            document.getElementById('balance-label').textContent = 'Balance: ' + data.balance;
        })
        .catch(() => {
            document.getElementById('balance-label').textContent = 'Balance: N/A';
        });
}

//Send transaciton handler
document
.getElementById('transaction-form')
.addEventListener('submit', function (e) {
    e.preventDefault();
    const amount = document.getElementById('amount').value;
    const to_account_id = document.getElementById('toAccountID').value;
    if (amount && to_account_id) {
        fetch('/send_transaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({amount, to_account_id }),
        })
        .then(async (response) => {
            const data = await response.json();
            if (response.ok) {
                document.getElementById('transaction-message').textContent =
                    data.message || 'Successfully sent ' + amount + ' to account ' + to_account_id + '.';
                document.getElementById('transaction-form').reset();
                alert('Successfully sent ' + amount + ' to account ' + to_account_id + '.');
                fetchAndDisplayBalance(); // Fetch and display balance after sending a transaction

            } else {
                document.getElementById('transaction-message').textContent =
                    data.detail || 'Invalid data.';
            }
        })
        .catch(() => {
            document.getElementById('transaction-message').textContent =
                'Something went wrong. Please try again later.';
        });
    }
});

//Load transactions
const loadBtn = document.getElementById('load-transactions');
const offerSpinner = document.getElementById('transactions-spinner');
const promoCards = document.querySelectorAll('.promo-card');
loadBtn.addEventListener('click', () => {
offerSpinner.classList.remove('hidden');
const grid = document.querySelector(".transactions-grid");
grid.innerHTML = "";
setTimeout(() => {
    offerSpinner.classList.add('hidden');
    loadTransactionsFromBackend()
}, 3000);
});

//Dynamic show of items
function renderTransactions(Transactions) {
    const grid = document.querySelector(".transactions-grid");
    grid.innerHTML = ""; // Clear previous content

    const table = document.createElement("table");
    table.className = "transactions-table";
    table.id = "transactions-table"; // Set ID for the table

    // Create table header
    const thead = document.createElement("thead");
    thead.innerHTML = "<tr><th>Email</th><th>To Account</th><th>Amount</th></tr>";
    table.appendChild(thead);

    // Create table body
    const tbody = document.createElement("tbody");
    Transactions.forEach(transaction => {
        const row = document.createElement("tr");
        row.className = "promo-card";
        
        row.innerHTML = `<td>${transaction.email}</td><td>${transaction["To Account"]}</td><td>${transaction.Amount}</td>`;

        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    grid.appendChild(table);
}

  function loadTransactionsFromBackend() {
  fetch('/view_transcaitons')
    .then(response => response.json())
    .then(data => renderTransactions(data))
    .catch(() => {
      // handle error
    });
}