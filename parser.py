import requests
import lxml, bs4

from PIL import Image, ImageDraw, ImageFont
from translate import Translator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Parser(object):
    """
    initialization of parser for requests library
    """

    def __init__(self, inquiry: str):
        total_inquiry = str("+".join(inquiry.split()))
        self.inquiry_ = total_inquiry.replace('+', '_')
        self.PRE = "https://www.google.com"
        if self.PRE not in inquiry:
            self.INQUIRY = f"""https://www.google.com/search?q={total_inquiry}"""
        else:
            self.INQUIRY = inquiry
        self.HEADERS = {
            "Accept": "* / *",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                          " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }

        self.html_text = requests.get(self.INQUIRY, self.HEADERS).text
        self.soup = bs4.BeautifulSoup(self.html_text, "lxml")  # полученный код штмл странички


class MainPage(Parser):
    """
    open images from main google paige
    """
    def __init__(self, inquiry: str):
        super().__init__(inquiry)
        self.up_tools = []
        self.up_link = []
        self.content = {}

    def main_page_tools(self):
        self.up_tools = self.soup.find_all("a", class_="eZt8xd")
        self.up_link = [i.get("href") for i in self.up_tools]
        itog = []
        for i in self.up_link:
            itog.append(self.PRE + i)

        return itog


class ImageParsing(MainPage):
    """ It downloads images """

    def __init__(self, inquiry: str):
        super().__init__(inquiry)
        total_inquiry = str("+".join(inquiry.split()))
        self.PRE = "https://www.google.com"
        if self.PRE not in inquiry:
            self.INQUIRY = f"""https://www.google.com/search?q={total_inquiry}"""
        else:
            self.INQUIRY = inquiry
        self.HEADERS = {
            "Accept": "* / *",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                          " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        EXE_PATH = r'chromedriver.exe'

        self.html_text = requests.get(self.INQUIRY, self.HEADERS).text
        self.soup = bs4.BeautifulSoup(self.html_text, "lxml")  # полученный код штмл странички
        parser = MainPage(inquiry)
        for _ in parser.main_page_tools():
            if "tbm=isch" in _:
                self.image_link = _

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(executable_path=EXE_PATH, chrome_options=options)
        driver.set_window_size(1440, 900)

        driver.get(str(self.image_link))
        driver.execute_script("""
                var elems = document.getElementsByClassName(" bRMDJf islir");
        elems[0].click();""")
        s = driver.page_source
        q = s
        self.res = []
        new = s.rfind('.png"')
        while new != -1:
            w = s[new - 100:new + 5]
            self.res.append(w[w.rfind('"https') + 1:-1])
            s = s[0:new - 10]
            new = s.rfind('.png"')
        self.res.pop(-1)
        self.res.pop(-1)
        self.res.pop(-1)
        # This is the way...

        new = q.rfind('.jpg"')
        while new != -1:
            w = q[new - 300:new + 5]
            self.res.append(w[w.rfind('"https') + 1:-1])
            q = q[0:new - 10]
            new = q.rfind('.jpg"')

    def download_image(self):
        # download 11 images by injure
        for i, url in enumerate(self.res):
            try:
                img = requests.get(url)
                img_file = open(f"images/{self.inquiry_}_{i}", 'wb')
                img_file.write(img.content)
                img_file.close()
                using_image = Image.open(f"images/{self.inquiry_}_{i}")
                translator = Translator(to_lang="German")
                translation = translator.translate(self.inquiry_.replace('_', ' '))
                font = ImageFont.truetype("arial.ttf", 50)
                drawer = ImageDraw.Draw(using_image)
                colour = [0, 0, 0]
                for x in range(using_image.size[1]):
                    for y in range(using_image.size[0]):
                        try:
                            r, g, b = using_image.getpixel((y, x))
                        except Exception:
                            r, g, b, _ = using_image.getpixel((y, x))
                        colour[0] += r
                        colour[1] += g
                        colour[2] += b
                for p in range(3):
                    colour[p] = (1 - round(colour[p] // (using_image.size[1] * using_image.size[0]) / 255)) * 255
                drawer.text(
                    (using_image.size[0] // 10, using_image.size[1] // 10), f"{translation}",
                    font=font,
                    fill="#" + ('{:X}{:X}{:X}').format(*colour)
                )
                using_image.resize((1920, 1080), Image.ANTIALIAS)

                using_image.save(f"images/{self.inquiry_}_{i}.png", format='PNG')
                using_image.close()
                # error in downloading image
                # or image is bad for being wallpaper
                if i >= 20:
                    # stop download
                    break
            except Exception as ex:
                print(ex)


if __name__ == "__main__":

    im_parser = ImageParsing(input())
    im_parser.download_image()
