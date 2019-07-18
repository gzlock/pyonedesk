# 发布到pypi

cd ./webpack
npm run build
cd ..
python3 setup.py bdist_wheel
# 发布
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
