const searchParams = new URLSearchParams(window.location.search)
const id = searchParams.get('id')

const title = document.querySelector('#event-title')
const description = document.querySelector('#event-description')
const date = document.querySelector('#date')
const oddsValue = document.querySelector('#odds-value')
const bettingStartDate = document.querySelector('#betting-start-date')
const bettingEndDate = document.querySelector('#betting-end-date')

const months = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
]

function formatGMT(gmt) {
  const date = new Date(gmt)

  return date.getDate() 
    + ' ' + months[date.getMonth()] 
    + ' ' + date.getFullYear()
}

fetch('http://localhost:5000/events/' + id, {
  method: 'GET',
  credentials: 'include',
})
.then((response) => {
  if (!response.ok) {
    // window.location.href = '/'
  }

  return response.json()
}).then((data) => {
  console.log(data)

  title.innerText = data.title
  description.innerText = data.description
  date.innerText = formatGMT(data.event_date),
  oddsValue.innerText = parseFloat(data.odds_value).toFixed(2)
  bettingStartDate.innerText = formatGMT(data.betting_start_date)
  bettingEndDate.innerText = formatGMT(data.betting_end_date)
})

function handleBetOnEvent(bet) {
  const amount = prompt('Enter the amount you want to bet on it')

  if (!Number(amount)) {
    return
  }

  fetch('http://localhost:5000/events/' + id + '/bets', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ amount: Number(amount), bet })
  }).then((response) => {
    if (response.status === 422) {
      alert('Transfer denied.')
      return
    }

    if (response.status !== 201) {
      alert('Uh oh! There was an error on our end. Please try again later.')
    }
  })
}

document.querySelector('#will-happen').addEventListener('click', () => handleBetOnEvent('yes'))
document.querySelector('#wont-happen').addEventListener('click', () => handleBetOnEvent('no'))