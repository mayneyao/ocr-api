import configparser
from io import BytesIO

import pytesseract
import requests

try:
    import Image
except ImportError:
    from PIL import Image

conf = configparser.ConfigParser()
conf.read('conf.ini')

TESSERACT_CMD = conf.get('TESSERACT', 'PATH')
LANG_DICT = {}

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def binarizing(img, threshold):  # input: gray image
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


def handle_img(img):
    # todo 图片处理 提高识别率
    # 灰度处理
    # img = img.convert('L')
    # 二值处理
    # img = binarizing(img, 127)
    # todo
    return img


def get_img(url):
    res = requests.get(url,stream=True)
    return Image.open(res.raw)


def get_text_from_img(img_url, lang):
    img = get_img(img_url)
    img = handle_img(img)
    return pytesseract.image_to_string(img, lang)


if __name__ == '__main__':
    test_img_url = 'https://lh3.googleusercontent.com/7wq4j5y-44hs8CvtsXe4nasK4Rif2bbm3qOhVE9IBPtTDtzbrAgW3O3kYPTO7utRwqZp2-zVfIv68h8KokrKEYTB8zAvyUfTr5xT0OPp3hrdrJi4QXG-78fFoLcX_IX63XjS-JwrDD5kDuFoD_WCQ5FxwSPDlL2eszHwNToKKvZJPyJ1ebqEIIqbGFscgjZXu3K6_LsLalkFgGWM8PjuCKTiI7c0r4EFTRYzmYoIifFVcS83Qjhpc6nJQk3y-LnORyx4h9dKpCyoXJB4rsSQuDbzj5xJ1uPHWz3dFVcRAEG9D-4EfVtGrIo0hjhV4VWVTmm1pcNsZvkEXWYrzCK_Y4C9YFrVJNLabKwQ4pVkiKB4pFsIrFwZoky4zZYb9SqWqICITNgVGmQ8RTbB8AgmmobsdGKVRLWidU7EheQBvKnbcmAgOEAzIv5rKbBJTzr3y2Je_N4aifH6WGMSF1dHqbGmwTxrVCKgw9HrmTV2G6EoozJlNXAg9JT58wJ9w-XSLgKUE95K8dQBCej2_7uRof5jRSqs2Nf0TbTO8waBtnAJLamATVNvdXBuS2N1uubeszxZLbTq_999S6d1Li6ikkREt9KEXUUFU3dydfo=w590-h926-no'
    text = get_text_from_img(test_img_url, 'chi_sim+en')
    print(text)
