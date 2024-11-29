const form = document.querySelector('#form')
const button = document.querySelector('#submit-button')

const name = document.querySelector('#name')
const description = document.querySelector('#description')
const oddsValue = document.querySelector('#odds-value')
const date = document.querySelector('#date')
const bettingStartDate = document.querySelector('#betting-start-date')
const bettingEndDate = document.querySelector('#betting-end-date')

form.addEventListener('submit', (event) => {
  event.preventDefault()

  button.innerHTML = 
    '<img class="animate-spin" width="16" height="16" src="/static/assets/loader-circle.svg" />'

  fetch('http://localhost:5000/events', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
      name: name.value,
      description: description.value,
      oddsValue: oddsValue.value,
      date: date.value,
      bettingStartDate: bettingStartDate.value,
      bettingEndDate: bettingEndDate.value,
    })
  })
  .then((response) => {
    if (response.status === 401) {
      alert('Incorrect email or password.')
      window.location.href = '/'

      return
    }

    if (response.status !== 201) {
      button.innerHTML = 'Submit'
      alert('Uh oh! There was an error on our end. Please try again later.')

      return
    }

    window.location.href = '/'
  })
})