config = {
    # 用来加解密管理后台的cookies token，✅建议自定义为更长更复杂的字符串✅
    'aes_key': 'PyOneDrive',
}

# 默认的样式数据，后台管理网页提供了丰富的自定义功能，⚠️不要修改这里的数据⚠️
stylizes = {
    # svg矢量图标
    'icon': {
        # iconfont.cn->我的项目->Symbol->js文件链接，这是兜底用的，不要修改
        'src': '//at.alicdn.com/t/font_1295827_bqjbq6h67tj.js',
        # 对应的是图标id
        'icons': {
            'default': 'py_white',
            'user': 'py_folder-personal',
            'folder': 'py_folder',
            'video': 'py_video',
            'audio': 'py_mp',
            'image': 'py_jpg',
            'text': 'py_txt',
            'code': 'py_html',
            'zip': 'py_zip',
            'pdf': 'py_pdf',
            'word': 'py_word',
            'excel': 'py_excel',
            'ppt': 'py_ppt',
        },
    },
    # 全局样式
    'css': 'body{ background: #99a9bf; }',
}
