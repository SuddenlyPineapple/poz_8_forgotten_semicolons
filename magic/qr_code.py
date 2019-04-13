import qrcode.image.svg
import qrtools

def gen_qrcode(code):
    code = str(code)
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(str(code), image_factory=factory)
    img.save(code+'.svg')


def decode_qrcode(image_link):
    qr = qrtools.QR()
    qr.decode(image_link)
    return qr.data
