
/**
 * Checks if the given text is a valid password, that is, if it has at least 8 
 * characters.
 * 
 * @param {string} text - The given text.
 * @returns {string | null} - The error message or nothing.
 * 
 */
export function isPassword(text) {
  return text.length < 8 ? 'Precisa de ao menos 8 caracteres' : null
}
