const form = document.querySelector('#form')
const button = document.querySelector('#submit-button')

const title = document.querySelector('#title')
const description = document.querySelector('#description')
const oddsValue = document.querySelector('#odds-value')
const date = document.querySelector('#date')
const bettingStartDate = document.querySelector('#betting-start-date')
const bettingEndDate = document.querySelector('#betting-end-date')

date.addEventListener('keypress', (e) => {
  if (e.keyCode < 47 || e.keyCode > 57) {
    e.preventDefault()
  }

  const len = e.target.value.length

  if (len !== 1 || len !== 3) {
    if (e.keyCode == 47) {
      e.preventDefault()
    }
  }
    
  if(len === 2 || len === 5) {
    e.target.value += '/'
  }
})

function maskAsDatetime(element) {
  element.addEventListener('input', (e) => {
    let value = e.target.value
    let formatted = value.replace(/\D/g, '')

    if (formatted.length > 2) {
      formatted = formatted.slice(0, 2) + '/' + formatted.slice(2)
    }

    if (formatted.length > 5) {
      formatted = formatted.slice(0, 5) + '/' + formatted.slice(5)
    }

    if (formatted.length > 10) {
      formatted = formatted.slice(0, 10) + ' ' + formatted.slice(10)
    }

    if (formatted.length > 13) {
      formatted = formatted.slice(0, 13) + ':' + formatted.slice(13, 15)
    }

    e.target.value = formatted
  })
}

maskAsDatetime(bettingStartDate)
maskAsDatetime(bettingEndDate)

function error(field, text) {
  const message = document.querySelector('#' + field + ' + .form__message')
  message.innerText = text
  
  if (button.innerHTML !== 'Submit') {
    button.innerHTML = 'Submit'
  }
}

function dateify(text) {
  const formatted =  text.split('/').toReversed().join('-')
  return formatted
}

function datetimeify(text) {
  console.log(text.length)

  if (text.length !== 16) {
    console.log('returning null')
    return null
  }

  const [datePart, timePart] = text.split(' ')
  const [day, month, year] = datePart.split('/').map(Number)
  const [hours, minutes] = timePart.split(':').map(Number)

  const date = new Date(Date.UTC(year, month - 1, day, hours, minutes))
  console.log('datetimeify: ' + date)
  return date
}

function isDateTime(text) {
  const date = datetimeify(text)
  return !isNaN(date.getTime())
}

function isDate(text) {
  const date = dateify(text)
  return !isNaN(new Date(date).getTime())
}

form.addEventListener('submit', (event) => {
  event.preventDefault()
  let hasError = false

  document.querySelectorAll('.form__message').forEach((e) => e.innerHTML = '')

  button.innerHTML = 
    '<img class="animate-spin" width="16" height="16" src="/static/assets/loader-circle.svg" />'

  if (!title.value) {
    error('name', 'Precisar ser fornecido.')
    hasError = true
  }

  if (title.value.length > 50) {
    error('name', 'Limite de 50 caracteres excedido.')
    hasError = true
  }

  if (description.value.length > 150) {
    error('description', 'Limite de 150 caracteres excedido.')
    hasError = true
  }

  if (+(oddsValue.value) < 1) {
    error('odds-value', 'Precisa ser ao menos R$ 1.')
    hasError = true
  }

  if (!isDate(date.value)) {
    error('date', 'Precisa fornecer uma data.')
    hasError = true
  }

  if (hasError) {
    button.innerHTML = 'Criar'
    return
  }

  console.log(bettingStartDate.value)
  console.log(datetimeify(bettingStartDate.value))

  fetch('http://localhost:5000/events', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
      title: title.value,
      description: description.value || '',
      odds_value: Number(oddsValue.value),
      event_date: dateify(date.value),
      betting_start_date: datetimeify(bettingStartDate.value),
      betting_end_date: datetimeify(bettingEndDate.value),
    })
  })
  .then((response) => {
    if (response.status !== 201) {
      button.innerHTML = 'Criar'
      alert('Ops! Houve um erro do nosso lado. Por favor, tente novamente mais tarde.')

      return
    }

    alert('Obrigado! Seu evento será avaliado pelos administradores.')
    window.location.href = '/'
  })
})