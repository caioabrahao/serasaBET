const EMAIL_REGEX = 
  /^(?!\.)(?!.*\.\.)([A-Z0-9_'+\-\.]*)[A-Z0-9_+-]@([A-Z0-9][A-Z0-9\-]*\.)+[A-Z]{2,}$/i

/**
 * Checks if the given text is a valid email address.
 * 
 * @param {string} text - The given text.
 * @returns {string | null} - The error message or nothing.
 * 
 */
export function isEmail(text) {
  return EMAIL_REGEX.test(text) ? null : 'Precisa ser uma email'
}
