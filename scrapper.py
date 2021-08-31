from bs4 import BeautifulSoup
import requests

class Annonce:
    def __init__(self, url: str, title: str, price: float, description: str = "", etat: str = "", shipping: bool = False, category: str = "", likes: int = 0, images: list = [], phone_number: str = "", email: str = "", location: str = "", publied_at: str = ""):
        self.title = title
        self.description = description
        self.price = price
        self.etat = etat
        self.shipping = shipping
        self.category = category
        self.likes = likes
        self.images = images
        self.phone_number = phone_number
        self.email = email
        self.location = location
        self.publied_at = publied_at
        self.url = url

class Scrapper:
    @staticmethod
    def search_by_title (title: str, min_price : int = 0, max_price : int = 10000, category : str = "") -> list[Annonce]:
        url = "https://affairespc.com/search?"
        url += "q="+ title
        url += "&price="+str(min_price)
        url += "%2C"+str(max_price)

        categories=['Processeur', 'Carte mère', 'Mémoire vive', 'Carte graphique', 'Ventirad', 'Watercooling', 'SSD M.2', 'SSD 2.5', 'Disque Dur', 'Boitier PC', 'Alimentation', 'Ventilateur', 'Ecran', 'Clavier', 'Souris', 'Tapis de souris', 'Casque', 'Siège gamer', 'Réseau', 'Kit', 'Enceinte', 'Microphone', 'Manette', 'Divers', 'PC Gamer', 'PC Portable', 'PC Portable Gamer', 'PC Bureautique']
        if category in categories:
            url += "&cat=" + str(categories.index(category)+2)
        
        url+="&order=new"

        return Scrapper.search_by_url(url)

    @staticmethod
    def search_by_url (url: str) -> list[Annonce]:
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')

        annonces_on_this_page: list[Annonce] = []
        for annonce in soup.findAll("div", {"class": "col-12 col-sm-6 col-md-4 col-lg-3 col-xl-3 p-0 effect-zoom-sm"}):
            url: str = annonce.find("a")["href"]
            title: str = annonce.find("div", {"class": "title mt-2"}).text
            price: float = float(annonce.find("div", {"class": "col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6 p-0 price text-center text-lg-left mb-2 mb-lg-0"}).text.replace("€", "").replace(" ", "").replace(",", "."))
            image : str = annonce.find("img", {"class": "rounded"})["src"]
            annonces_on_this_page.append(Annonce(url, title, price, images=[image]))
        return annonces_on_this_page

    @staticmethod
    def get_this_page (url: str) -> Annonce:  
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')

        title = soup.find("h1", {"class": "main-title h3"}).text
        

        description = soup.find("div", {"class": "col-12 p-1 text-left"}).find('p').text
        

        price = float(soup.find("div", {"class": "mb-1 h2 text-primary"}).text.replace("€", "").replace(",", ".").replace(" ", ""))
        

        info = soup.find("div", {"class": "col-12 p-1 text-center"}).findAll("div")

        category = info[0].text
        

        publied_at = info[1].text
        

        etat = info[2].text
        

        likes = int(info[3].text)
        

        shipping = "Envoi" in soup.find("div", {"class": "mb-1 d-inline-block"}).text
        

        images_scraped = soup.find("div", {"class": "carousel-inner"}).findAll("div")
        images = []
        for i in images_scraped:
            images.append(str(i).replace('<div class="carousel-item active" style="height:500px;background-image:url(', "").replace('<div class="carousel-item" style="height:500px;background-image:url(', "").replace(');background-size: contain;background-repeat: no-repeat;background-position: center;"></div>', "").replace("'", ""))
        

        location = soup.find("div", {"class": "mb-1 d-inline-block mr-2"}).text
        

        contact = soup.find("div", {"class": "col-12 col-md-4 p-1 text-center"}).findAll("button")

        id = url.split("-")[-1]

        email = str(contact[0]).replace('<button class="btn btn-outline-primary btn-xs btn-block shadow-sm" id="btn_view_email" onclick="display_text(this,', "").replace(f');add_clic_annonce({id});">Voir l', "").replace('email</button>', "").replace("'", "")

        phone_number = str(contact[1]).replace('<button class="btn btn-outline-primary btn-xs btn-block shadow-sm" id="btn_view_phone" onclick="display_text(this,', "").replace(f');add_clic_annonce({id});">Voir le numéro</button>', "").replace("'", "")

        return Annonce(url, title, price, description, etat, shipping, category, likes, images, phone_number, email, location, publied_at)

