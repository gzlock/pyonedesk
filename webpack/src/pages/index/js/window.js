export const WindowEvent = Object.freeze({
  FileUploaded: Symbol('uploaded'),
  FileDeleted: Symbol('deleted'),
  SortFile: Symbol('sort'),
  SearchFile: Symbol('search'), // 参数 {type:FileSortType,isUp:bool}
})

export class Window {
  constructor(user, file, z) {
    this.id = Date.now().toString(32)
    this.user = user
    this.file = file
    this.z = z
    this.events = {}
  }

  /**
   *
   * @param event
   * @param callback
   */
  addEventListener(event, callback) {
    if(!this.events[event])
      this.events[event] = []
    this.events[event].push(callback)
  }

  /**
   *
   * @param event
   * @param callback
   */
  removeEventListener(event, callback) {
    if(this.events[event]) {
      const index = this.events[event].indexOf(callback)
      if(index > -1)
        this.events[event].splice(index, 1)
    }
  }

  /**
   *
   * @param event
   * @param data
   */
  trigger(event, data) {
    if(this.events[event])
      this.events[event].forEach(cb => cb(data))
  }

  /**
   *
   * @param event
   */
  clearEventListener(event = null) {
    if(event)
      this.events[event] = []
    else
      this.events = {}
  }

}