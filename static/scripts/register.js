import { validate } from './utils/validate.js'
import { isDateOfBirth } from './utils/is-date-of-birth.js'
import { isNotEmpty } from './utils/is-not-empty.js'
import { isEmail } from './utils/is-email.js'
import { isPassword } from './utils/is-password.js'

const dateOfBirth = document.querySelector('#date-of-birth')

const form = document.querySelector('.form')
const button = document.querySelector('.button')

dateOfBirth.addEventListener('keypress', (e) => {
  if (e.keyCode < 47 || e.keyCode > 57) {
    e.preventDefault()
  }

  const len = dateOfBirth.value.length
    
  if (len !== 1 || len !== 3) {
    if (e.keyCode == 47) {
      e.preventDefault()
    }
  }
    
  if(len === 2 || len === 5) {
    dateOfBirth.value += '/'
  }
})

form.addEventListener('submit', (event) => {
  event.preventDefault()

  const result = validate({
    name: [isNotEmpty],
    'date-of-birth': [isDateOfBirth],
    email: [isEmail],
    password: [isPassword],
  })

  if (!result.success) {
    return
  }

  button.innerHTML = 
    '<img class="animate-spin" width="16" height="16" src="/static/assets/loader-circle.svg" />'

  fetch('http://localhost:5000/register', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: result.data.name,
      'date_of_birth': result.data['date-of-birth']
        .split('/')
        .toReversed()
        .join('-'),
      email: result.data.email, 
      password: result.data.password,
    })
  })
  .then((response) => {
    if (response.status === 409) {
      alert('Email already in use. Maybe you should log in instead.')
      button.innerHTML = 'Register'

      return
    }

    if (response.status !== 201) {
      alert('Uh oh! There was an error on our end. Please try again later.')
      button.innerHTML = 'Register'

      return
    }

    window.location.href = '/'
  })
})
