import { get } from 'lodash'

export const FileType = Object.freeze({
  Normal: Symbol('normal'),
  Image: Symbol('image'),
  Audio: Symbol('audio'),
  Video: Symbol('video'),
  Text: Symbol('text'),
  Code: Symbol('code'),
  Word: Symbol('word'),
  Excel: Symbol('excel'),
  PPT: Symbol('ppt'),
  Zip: Symbol('zip'),
  Folder: Symbol('folder'),
  PDF: Symbol('pdf'),
})
export const FileState = Object.freeze({
  Normal: Symbol('normal'),//正常状态
  Uploading: Symbol('uploading'),//上传文件中
  Waiting: Symbol('waiting'),//上传文件队列等待
  Deleting: Symbol('deleting'),//正在删除文件
  UploadFail: Symbol('uploadFail'),//上传失败
})

// https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Complete_list_of_MIME_types

const wordMimeType = [
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
]
const excelMimeType = [
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
]
const pptMimeType = [
  'application/vnd.ms-powerpoint',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation',
]
const zipMimeType = [
  'application/zip',
  'application/x-7z-compressed',
  'application/x-rar-compressed',
  'application/x-tar',
  'application/x-bzip',
  'application/x-bzip2',
]

function fileNameToType(name, list) {
  console.log('fileNameToType', name)
  for(let i = 0; i < list.length; i++) {
    if(name.lastIndexOf(list[i]) !== -1)
      return true
  }
  return false
}

const codeFormats = [
  '.py',
  '.cs',
  '.c',
  '.htm',
  '.js',
  '.xml',
  '.php',
  '.jsp',
  '.rb',
  '.pl',
  '.asp',
  '.ini',
  '.cg',
  '.java',
  '.as',
  '.config',
  '.hh',
  '.hs',
  '.css',
  '.scss',
  '.sass',
]

export class File {
  constructor(name, path, mimeType) {
    this.name = name
    this.mimeType = mimeType
    this.path = path.replace(/\/+/g, '/')
    // console.log('file', path, this.path)
    this.thumbnail = null
    this.id = null
  }

  setType(type = null) {
    if(type) {
      this.type = type
    } else {
      if(!this.mimeType)
        this.type = FileType.Folder
      else if(this.mimeType.indexOf('image/') !== -1)
        this.type = FileType.Image
      else if(this.mimeType.indexOf('audio/') !== -1)
        this.type = FileType.Audio
      else if(this.mimeType.indexOf('video/') !== -1)
        this.type = FileType.Video
      else if(fileNameToType(this.name, codeFormats))
        this.type = FileType.Code
      else if(wordMimeType.indexOf(this.mimeType) !== -1)
        this.type = FileType.Word
      else if(excelMimeType.indexOf(this.mimeType) !== -1)
        this.type = FileType.Excel
      else if(pptMimeType.indexOf(this.mimeType) !== -1)
        this.type = FileType.PPT
      else if(zipMimeType.indexOf(this.mimeType) !== -1)
        this.type = FileType.Zip
      else if(this.mimeType === 'text/plain')
        this.type = FileType.Text
      else if(this.mimeType === 'application/pdf')
        this.type = FileType.PDF
      else
        this.type = FileType.Normal
    }
    return this
  }

  setFromData(data) {
    const thumbnail = get(data, 'thumbnails[0].small.url')
    if(thumbnail) {
      this.thumbnail = thumbnail
    }
    this.id = data.id
    this.mimeType = get(data, 'file.mimeType')
    if(data['parentReference'])
      this.path = data['parentReference']['path'] === '/drive/root:'
        ? '/'
        : data['parentReference']['path'].replace('/drive/root:', '/')
    return this
  }

  setState(state) {
    this.state = state
    return this
  }
}