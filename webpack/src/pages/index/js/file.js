export const FileType = Object.freeze({
  Normal: Symbol('normal'),
  Image: Symbol('image'),
  Audio: Symbol('audio'),
  Video: Symbol('Video'),
  Text: Symbol('text'),
  Code: Symbol('Code'),
  Word: Symbol('word'),
  Excel: Symbol('excel'),
  PPT: Symbol('ppt'),
  Zip: Symbol('zip'),
  Folder: Symbol('folder'),
  PDF: Symbol('pdf'),
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
  constructor(name, path, mimeType, thumbnail) {
    this.name = name
    this.mimeType = mimeType
    if(!mimeType)
      this.type = FileType.Folder
    else if(mimeType.indexOf('image/') !== -1)
      this.type = FileType.Image
    else if(mimeType.indexOf('audio/') !== -1)
      this.type = FileType.Audio
    else if(mimeType.indexOf('video/') !== -1)
      this.type = FileType.Video
    else if(fileNameToType(name, codeFormats))
      this.type = FileType.Code
    else if(wordMimeType.indexOf(mimeType) !== -1)
      this.type = FileType.Word
    else if(excelMimeType.indexOf(mimeType) !== -1)
      this.type = FileType.Excel
    else if(pptMimeType.indexOf(mimeType) !== -1)
      this.type = FileType.PPT
    else if(zipMimeType.indexOf(mimeType) !== -1)
      this.type = FileType.Zip
    else if(mimeType === 'text/plain')
      this.type = FileType.Text
    else if(mimeType === 'application/pdf')
      this.type = FileType.PDF
    else
      this.type = FileType.Normal
    this.path = path
    this.thumbnail = thumbnail
  }
}