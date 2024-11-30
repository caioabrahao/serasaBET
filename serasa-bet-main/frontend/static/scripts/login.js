import { validate } from './utils/validate.js'
import { isEmail } from './utils/is-email.js'
import { isNotEmpty } from './utils/is-not-empty.js'

const form = document.querySelector('.form')
const button = document.querySelector('.button')

form.addEventListener('submit', (event) => {
  event.preventDefault()

  const result = validate({
    email: [isEmail],
    password: [isNotEmpty],
  })

  if (!result.success) {
    return
  }

  button.innerHTML = 
    '<img class="animate-spin" width="16" height="16" src="/static/assets/loader-circle.svg" />'

  fetch('http://localhost:5000/login', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ 
      email: result.data.email, 
      password: result.data.password 
    })
  })
  .then((response) => {
    if (response.status === 401) {
      alert('Incorrect email or password.')
      button.innerHTML = 'Login'

      return
    }

    if (response.status !== 201) {
      button.innerHTML = 'Login'
      alert('Ops! Houve um erro do nosso lado. Por favor, tente novamente mais tarde.')

      return
    }

    window.location.href = '/'
  })
})