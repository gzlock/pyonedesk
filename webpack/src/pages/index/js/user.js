export class User {
  constructor(id, name, lock = false) {
    this.id = id
    this.name = name
    this.lock = lock
  }
}