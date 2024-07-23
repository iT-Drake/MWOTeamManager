### Library issues

Chromium version that is used by a pyppeteer library is hardcoded in __init__.py file:
```python
__chromium_revision__ = '1181205'
```

Recently it was removed from a google storage. Try to replace the version with something newer: '1263111'.
Or set environmental variable:
```shell
PYPPETEER_CHROMIUM_REVISION = '1263111'
```

Thread: https://stackoverflow.com/questions/78023508/python-request-html-is-not-downloading-chromium
