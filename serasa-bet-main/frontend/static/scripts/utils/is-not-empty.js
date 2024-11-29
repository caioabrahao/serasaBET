
/**
 * Checks if the given text is not an empty string, that is, if it has at least 1 character. Notice that the validate 
 * function automatically trim values, so a string like " " will not pass this validator.
 * 
 * @param {string} text The given text.
 * @returns {string | null} The error message or nothing.
 * 
 */
export function isNotEmpty(text) {
  return text.length === 0 ? 'Field is required.' : null
}
