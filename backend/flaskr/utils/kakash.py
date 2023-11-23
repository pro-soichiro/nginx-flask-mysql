import pykakasi

class Kakash:
    kks = pykakasi.kakasi()
    kks.setMode('H', 'a')
    kks.setMode('K', 'a')
    kks.setMode('J', 'a')
    conv = kks.getConverter()

    @classmethod
    def japanese_to_ascii(cls, text):
      return cls.conv.do(text)