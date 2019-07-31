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
export const FileSortType = Object.freeze({
  Name: Symbol('name'),
  Size: Symbol('size'),
  CreatedTime: Symbol('ctime'),
  ModifiedTime: Symbol('mtime'),
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
      this.type = GetFileType(this.name, this.mimeType)
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
    const path = get(data,'parentReference.path')
    if(path)
      this.path = path === '/drive/root:'? '/':
        path.replace('/drive/root:', '/')
    return this
  }

  setState(state) {
    this.state = state
    return this
  }

  clone() {
    return new File(this.name, this.path, this.mimeType)
  }
}

export const defaultSort = { type: FileSortType.Name, isUp: false }

/**
 *
 * @param fileName
 * @param mimeType
 * @returns {FileType}
 */
export function GetFileType(fileName, mimeType) {
  let type
  if(!mimeType)
    type = FileType.Folder
  else if(mimeType.indexOf('image/') !== -1)
    type = FileType.Image
  else if(mimeType.indexOf('audio/') !== -1)
    type = FileType.Audio
  else if(mimeType.indexOf('video/') !== -1)
    type = FileType.Video
  else if(fileNameToType(fileName, codeFormats))
    type = FileType.Code
  else if(wordMimeType.indexOf(mimeType) !== -1)
    type = FileType.Word
  else if(excelMimeType.indexOf(mimeType) !== -1)
    type = FileType.Excel
  else if(pptMimeType.indexOf(mimeType) !== -1)
    type = FileType.PPT
  else if(zipMimeType.indexOf(mimeType) !== -1)
    type = FileType.Zip
  else if(mimeType === 'text/plain')
    type = FileType.Text
  else if(mimeType === 'application/pdf')
    type = FileType.PDF
  else
    type = FileType.Normal
  return type
}