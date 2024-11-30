let balance = null

async function renderBalance() {
  const response = await fetch('http://localhost:5000/wallet/balance', {
    method: 'GET',
    credentials: 'include',
  })

  const data = await response.json()
  balance = Number(data.balance)

  document.querySelector('#balance').innerText = 
    'R$ ' + parseFloat(data.balance).toFixed(2)
}

async function renderBetCount() {
  const response = await fetch('http://localhost:5000/wallet/bet-count', {
    method: 'GET',
    credentials: 'include',
  })

  const data = await response.json()

  document.querySelector('#bet-count').innerText = data.count
}

function brl(decimal) {
  const number = parseFloat(decimal)

  const formatted = new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(number)

  return formatted
}

function formatDate(date) {
  const options = { 
    day: 'numeric', 
    month: 'long', 
    year: 'numeric' 
  }

  const formatted = new Intl.DateTimeFormat('pt-BR', options).format(date);

  return formatted.replace(/ de /g, ' de ')
}

function renderHistoryItem({ type, amount, date }) {
  return `
    <tr class="table__row">
      <td class="table__cell">${type.replace(/^[a-z]/, (l) => l.toUpperCase())}</td>
      <td class="table__cell">${brl(amount)}</td>
      <td class="table__cell">${formatDate(date)}</td>
    </tr>
  `
}

async function renderHistory() {
  const response = await fetch('http://localhost:5000/wallet/history', {
    method: 'GET',
    credentials: 'include',
  })

  const data = await response.json()

  document.querySelector('#history').innerHTML = data.history.reduce(
    (acc, cur) => {
      return acc + renderHistoryItem(cur)
    },
    ''
  )
}

async function populate(params) {
  await Promise.all([
    renderBalance(),
    renderBetCount(),
    renderHistory(),
  ])
}

populate()

function deposit(number) {
  fetch('http://localhost:5000/wallet/deposit', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ amount: number }),
  })
  .then(() => {
    balance = balance + number
    document.querySelector('#balance').innerText = 'R$ ' + parseFloat(balance).toFixed(2)
  })
}

function withdraw(number) {
  fetch('http://localhost:5000/wallet/withdraw', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ amount: number }),
  })
  .then(() => {
    balance = balance - number
    document.querySelector('#balance').innerText = 'R$ ' + parseFloat(balance).toFixed(2)
  })
}

function transfer(type) {
  const el = document.querySelector('#' + type + '-amount')
  const amount = Number(el.value)

  if (type === 'withdraw') {
    withdraw(amount)
  }

  if (type === 'deposit') {
    deposit(amount)
  }
}

document.querySelector('#withdraw-form').addEventListener('submit', (event) => {
  event.preventDefault()
  transfer('withdraw')
  MicroModal.close('withdraw-modal')
})

document.querySelector('#deposit-form').addEventListener('submit', (event) => {
  event.preventDefault()
  transfer('deposit')
  MicroModal.close('deposit-modal')
})

document.querySelector('#deposit-button').addEventListener('click', () => {
  MicroModal.show('deposit-modal')
})

document.querySelector('#withdraw-button').addEventListener('click', () => {
  MicroModal.show('withdraw-modal')
})