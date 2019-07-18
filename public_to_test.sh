
cd ./webpack
npm run build
cd ..
python3 setup.py bdist_wheel
# 发布
# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# 依赖 ~/.pypirc 账号密码
python3 -m twine upload -r test_pypi dist/*