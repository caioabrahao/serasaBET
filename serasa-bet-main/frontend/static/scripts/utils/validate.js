/**
 * @typedef {Object} Success
 * @property {boolean} success - The flag indicating success (true).
 * @property {Record<string, unknown>} data - The data returned on success.
 */

/**
 * @typedef {Object} Failure
 * @property {boolean} success - The flag indicating failure (false).
 */

/**
 * @typedef {Success | Failure} Result - The union type of Success or Failure.
 */

/**
 * Executes the provided validations for each input.
 * 
 * @param {Record<string, (() => string | null)[]} inputs
 * @param {(() => string | null)[]} inputs[].
 * @returns {Result} result
 */
export function validate(inputs) {
  const result = {
    success: true,
    data: {}
  }

  for (const [name, validators] of Object.entries(inputs)) {
    const input = document.querySelector('#' + name)
    const message = document.querySelector('#' + name + ' + .form__message')

    for (const validator of validators) {
      const value = input.value.trim()
      const validation = validator(value)
      
      if (typeof validation === 'string') {
        message.innerText = validation

        result.success = false
        delete result.data

        break
      }

      message.innerText = ''

      if (result.success) {
        result.data[name] = value
      }
    }
  }

  return result
}
