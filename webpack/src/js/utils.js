/**
 * 字节转为对应的容量单位
 * @param bytes
 * @returns {string}
 */
export function bytesToSize(bytes) {
  if(bytes === 0) return '0 B'
  const k = 1024, // or 1024
    sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
    i = Math.floor(Math.log(bytes) / Math.log(k))

  return (bytes / Math.pow(k, i)).toPrecision(3) + ' ' + sizes[i]
}