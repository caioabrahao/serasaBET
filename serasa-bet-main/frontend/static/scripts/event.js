const searchParams = new URLSearchParams(window.location.search)
const id = searchParams.get('id')

const title = document.querySelector('#event-title')
const description = document.querySelector('#event-description')
const date = document.querySelector('#date')
const oddsValue = document.querySelector('#odds-value')
const bettingStartDate = document.querySelector('#betting-start-date')
const bettingEndDate = document.querySelector('#betting-end-date')

const months = [
  'Janeiro',
  'Fevereiro',
  'Março',
  'Abril',
  'Maio',
  'Junho',
  'Julho',
  'Agosto',
  'Setembro',
  'Outubro',
  'Novembro',
  'Dezembro',
]

function formatGMT(gmt) {
  const date = new Date(gmt)

  return date.getDate() 
    + ' de ' + months[date.getMonth()] 
    + ' de ' + date.getFullYear()
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
  const amount = prompt('Digite a quantia que você gostaria de apostar nisso')

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
      alert('Não foi possível completar a transação, verifique seu saldo e o período de apostas.')
      return
    }

    if (response.status !== 204) {
      alert('Ops! Houve um erro do nosso lado. Por favor, tente novamente mais tarde.')
    }

    alert('Obrigado! Sua aposta foi computada.')
  })
}

document.querySelector('#will-happen').addEventListener('click', () => handleBetOnEvent('yes'))
document.querySelector('#wont-happen').addEventListener('click', () => handleBetOnEvent('no'))