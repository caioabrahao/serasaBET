
/**
 * Checks if the given text is not an empty string, that is, if it has at least 1 character. Notice that the validate 
 * function automatically trim values, so a string like " " will not pass this validator.
 * 
 * @param {string} text The given text.
 * @returns {string | null} The error message or nothing.
 * 
 */
export function isDateOfBirth(text) {
  if (text.length !== 10) {
    return 'Precisa ser válida'
  }

  const [day, month, year] = text.split('/').map(Number)
  const date = new Date(year, month - 1, day)

  const now =  new Date()
  now.setHours(0, 0, 0, 0)

  return date >= now ? 'Precisa estar no passado' : null
}
