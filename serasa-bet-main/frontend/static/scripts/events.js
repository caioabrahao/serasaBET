const input = document.querySelector('#search-input')
const form = document.querySelector('#search-form')
const list = document.querySelector('#event-list')

const searchParams = new URLSearchParams(window.location.search)
const search = searchParams.get('search') ?? ''

input.value = search

function renderEventCard({ id, title, description, odds_value, bet_count }) {
  return `
    <li class="scrollable-section__item">
      <a class="no-decoration" href="/event?id=${id}">
        <div class="card event-card">
          <div class="card__title">${title}</div>
          <div class="card__description">${description}</div>

          <div class="event-card__info">
            <div class="event-card__info-text">
              R$ ${parseFloat(odds_value).toFixed(2)}
            </div>
          </div>
        </div>
      </a>
    </li>
  `
}

function handleSearch(search) {
  fetch('http://localhost:5000/events?search=' + search, {
    method: 'GET',
    credentials: 'include'
  })
  .then((response) => {
    if (response.status !== 200) {
      alert('Ops! Houve um erro do nosso lado. Por favor, tente novamente mais tarde.')
      return
    }

    return response.json()
  }).then((data) => {
    list.innerHTML = data.events.reduce((acc, cur) => {
      return acc + renderEventCard(cur)
    }, '')
  })
}

handleSearch(search)

form.addEventListener('submit', (event) => {
  event.preventDefault()

  const searchParams = new URLSearchParams(window.location.search)
  searchParams.set('search', input.value)
  window.history.replaceState(null, '', '?' + searchParams.toString())

  handleSearch(input.value)
})