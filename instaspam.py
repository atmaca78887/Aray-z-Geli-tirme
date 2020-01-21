# coding=utf-8
#!/usr/bin/env python3

""" 
Programı değiştirip bir yerde yayınlamadan önce lütfen
bu programın GPLv3 lisansı altında olduğunu unutmayınız.
Daha Fazla Bilgi:
https://tr.wikipedia.org/wiki/GNU_Genel_Kamu_Lisans%C4%B1
https://www.gnu.org/licenses/quick-guide-gplv3.html
"""

__author__ = "Hichigo TurkHackTeam"
__license__ = "GPLv3"
__version__ = "2.1.0"
__status__ = "Geliştiriliyor"



from time import time, sleep
from random import choice
from multiprocessing import Process
from PyQt5.QtWidgets import QVBoxLayout,QWidget,QLayout,QLabel,QLabel,QLineEdit,QComboBox,QPushButton,QApplication
import sys

from libs.utils import CheckPublicIP, IsProxyWorking
from libs.utils import PrintStatus, PrintSuccess, PrintError
from libs.utils import PrintBanner, GetInput, PrintFatalError
from libs.utils import LoadUsers, LoadProxies, PrintChoices

from libs.instaclient import InstaClient

USERS = []
PROXIES = []

def MultiThread(username, userid, loginuser, loginpass, proxy, reasonid):
    client = None
    if (proxy != None):
        PrintStatus("[" + loginuser + "]", "Hesaba Giriş Yapılıyor!")
        client = InstaClient(
            loginuser,
            loginpass,
            proxy["ip"],
            proxy["port"]
        )
    else:
        PrintStatus("[" + loginuser + "]", "Hesaba Giriş Yapılıyor!")
        client = InstaClient(
            loginuser,
            loginpass,
            None,
            None
        )
        
    client.Connect()
    client.Login()
    client.Spam(userid, username, reasonid)
    print("")

def NoMultiThread():
    for user in USERS:
        client = None
        if (useproxy):
            proxy = choice(PROXIES)
            PrintStatus("[" + user["user"] + "]", "Hesaba Giriş Yapılıyor!")
            client = InstaClient(
                user["user"],
                user["password"],
                proxy["ip"],
                proxy["port"]
            )
        else:
            proxy = choice(PROXIES)
            PrintStatus("[" + user["user"] + "]", "Hesaba Giriş Yapılıyor!")
            client = InstaClient(
                user["user"],
                user["password"],
                None,
                None
            )
        
        client.Connect()
        client.Login()
        client.Spam(userid, username, reasonid)
        print("")


if __name__ == "__main__":
    class Ekran(QWidget):
        def __init__(self):
            super().__init__()

            self.devam()

        def devam(self):
            self.anase = QLabel("""

                        _.._
                      .' .-'`
                     /  /         THT Instagram Spam Script'i
                     |  |         ---------------------------
                     \  '.___.;      Yapımcı: Hichigo THT
                      '._  _.'
                         ``
                    """)

            self.kadyaz = QLabel("Şikayet Edilecek Kullanıcının Adı :")
            self.kad = QLineEdit()

            self.henyaz = QLabel("Şikayet etmek istediğiniz hesap numarası: ")
            self.hen = QLineEdit()

            self.ehyaz = QLabel("Proxy kullanmak ister misin?")
            self.eh = QComboBox(self)
            self.eh.addItem("Evet")
            self.eh.addItem("Hayır")

            self.mudyaz = QLabel(
                "Multithreading kullanmak ister misin? (Çok fazla kullanıcınız varsa veya bilgisayarınız yavaşsa bu özelliği kullanmayın!): ")
            self.mud = QComboBox(self)
            self.mud.addItem("Evet")
            self.mud.addItem("Hayır")

            self.nednamaa = QLabel(
                " Spam = 1 \n\n Kendine Zarar Verme = 2 \n\n Uyuşturucu = 3 \n\n Çıplaklık = 4 \n\n Şiddet = 5 \n\n Nefret Söylemi = 6 \n\n Taciz ve Zorbalık = 7 \n\n Kimlik Taklidi = 8 \n\n Yaşı Tutmayan Çocuk = 11\n"
                )
            self.nednamyaz = QLabel("Lütfen üstteki şikayet nedenlerinden birini seçin (örn: spam için 1): ")
            self.nednam = QComboBox(self)
            a = ["1", "2", "3", "4", "5", "6", "7", "8", "11"]
            self.nednam.addItems(a)

            self.bitir = QPushButton("Atağı Başlat")

            self.durum = QLabel("Henüz başlanmadı!")

            vbox = QVBoxLayout()
            vbox.addWidget(self.anase)
            vbox.addWidget(self.kadyaz)
            vbox.addWidget(self.kad)
            vbox.addStretch()
            vbox.addWidget(self.henyaz)
            vbox.addWidget(self.hen)
            vbox.addStretch()
            vbox.addWidget(self.ehyaz)
            vbox.addWidget(self.eh)
            vbox.addStretch()
            vbox.addWidget(self.mudyaz)
            vbox.addWidget(self.mud)
            vbox.addStretch()
            vbox.addWidget(self.nednamaa)
            vbox.addWidget(self.nednamyaz)
            vbox.addWidget(self.nednam)
            vbox.addStretch()

            vbox.addWidget(self.durum)
            vbox.addWidget(self.bitir)

            self.setLayout(vbox)
            self.setGeometry(400, 40, 300, 300)
            self.setWindowTitle("İnstaSpam v2.1")
            self.show()

            self.bitir.clicked.connect(self.aq)
        def aq(self):

            USERS = LoadUsers("./kullanicilar.txt")
            PROXIES = LoadProxies("./proxyler.txt")

            username = self.kad.text()
            userid = self.hen.text()
            useproxy = self.eh.currentText()
            if (useproxy == "Evet"):
                useproxy = True
            elif (useproxy == "Hayır"):
                useproxy = False
            else:
                PrintFatalError("Lütfen sadece 'Evet' yada 'Hayır' girin!")
                exit(0)
            usemultithread = self.mud.currentText()

            if (usemultithread == "Evet"):
                usemultithread = True
            elif (usemultithread == "Hayır"):
                usemultithread = False
            else:
                PrintFatalError("Lütfen sadece 'Evet' yada 'Hayır' girin!")
                exit(0)

            PrintChoices()
            reasonid = self.nednam.currentText()
            self.durum.setText("Başlıyor.")
            if (usemultithread == False):
                NoMultiThread()
            else:
                for user in USERS:
                    p = Process(target=MultiThread,
                                args=(username,
                                      userid,
                                      user["user"],
                                      user["password"],
                                      None if useproxy == False else choice(PROXIES),
                                      reasonid
                                      )
                                )
                    p.start()


    app = QApplication(sys.argv)
    aaaa = Ekran()
    sys.exit(app.exec_())
