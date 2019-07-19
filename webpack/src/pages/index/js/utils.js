/**
 * async/await 等待
 * @param millionsSeconds
 * @returns {Promise<any>}
 */
export function Wait(millionsSeconds) {
  return new Promise(resolve => {
    setTimeout(() => {resolve()}, millionsSeconds)
  })
}