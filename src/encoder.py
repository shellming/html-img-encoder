import base64
import os
from bs4 import BeautifulSoup

def guess_type(filepath):
    """
    Return the mimetype of a file, given it's path.
    This is a wrapper around two alternative methods - Unix 'file'-style
    magic which guesses the type based on file content (if available),
    and simple guessing based on the file extension (eg .jpg).
    :param filepath: Path to the file.
    :type filepath: str
    :return: Mimetype string.
    :rtype: str
    """
    try:
        import magic  # python-magic
        return magic.from_file(filepath, mime=True)
    except ImportError:
        import mimetypes
        return mimetypes.guess_type(filepath)[0]

def encode(img_path):
    with open(img_path, "rb") as img_file:
        encode_str = base64.b64encode(img_file.read())
    return encode_str.decode("utf-8")


def inline_img(base_dir, input, output):
    input_path = os.path.join(base_dir, input)
    output_path = os.path.join(base_dir, output)
    with open(input_path, 'r') as input_file:
        soup = BeautifulSoup(input_file, 'html.parser')
        for img in soup.find_all('img'):
            if '.' not in img.attrs['src']:
                continue
            img_path = os.path.join(base_dir, img.attrs['src'])
            mimetype = guess_type(img_path)
            img_encoded = encode(img_path)
            img.attrs['src'] = \
                "data:%s;base64,%s" % (mimetype, img_encoded)

    with open(output_path, 'w') as of:
        of.write(str(soup))


if __name__ == '__main__':
    inline_img('/home/wangming/code/offer/el/s9/eata-mt', 'index_raw.html', 'index.html')
