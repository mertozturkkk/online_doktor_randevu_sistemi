"""
  Online Doktor Randevu Sistemi

Sınıflar:
  - Hasta          : Hasta bilgileri ve randevu geçmişi
  - Doktor         : Doktor bilgileri, müsait saatler, puanlama
  - Randevu        : Randevu oluşturma ve iptal
  - RandevuSistemi : Tüm akışı yöneten ana sistem sınıfı

Ek Özellikler:
  - Şikayet notu
  - Doktor puanlama sistemi (1-5)
  - Doktora göre günlük randevu filtresi
  - Girdi doğrulama (TC, saat formatı, yaş, tarih)
  - Aynı hastanın aynı güne çift randevu engeli
  - Aynı TC ile tekrar kayıt engeli
"""

from datetime import datetime


#  YARDIMCI FONKSİYONLAR


def tc_dogrula(tc):
    """TC kimlik numarası 11 haneli ve sayısal olmalı."""
    return tc.isdigit() and len(tc) == 11

def saat_dogrula(saat):
    """Saat HH:MM formatinda olmali (orn: 09:30)."""
    try:
        datetime.strptime(saat, "%H:%M")
        return True
    except ValueError:
        return False

def tarih_dogrula(tarih):
    """Tarih GG.AA.YYYY formatinda olmali."""
    try:
        datetime.strptime(tarih, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def int_al(mesaj, min_val=None, max_val=None):
    """Kullanıcıdan guvenli sekilde tam sayi alir. Gecersiz girisde None doner."""
    try:
        deger = int(input(mesaj))
        if min_val is not None and deger < min_val:
            print(f"  En az {min_val} olmali.")
            return None
        if max_val is not None and deger > max_val:
            print(f"  En fazla {max_val} olmali.")
            return None
        return deger
    except ValueError:
        print("  Lutfen gecerli bir sayi girin.")
        return None



#  HASTA SINIFI


class Hasta:
    def __init__(self, hasta_id, ad, tc, telefon, yas):
        self.hasta_id   = hasta_id
        self.ad         = ad
        self.tc         = tc
        self.telefon    = telefon
        self.yas        = yas
        self.randevular = []        # Hastanin aldigi randevular listesi

    def randevu_al(self, randevu):
        """Hastanin randevu listesine yeni randevu ekler."""
        self.randevular.append(randevu)

    def randevu_gecmisi(self):
        """Hastanin tum randevularini listeler (aktif ve iptal)."""
        aktif = [r for r in self.randevular if r.durum == "Aktif"]
        iptal = [r for r in self.randevular if r.durum == "Iptal"]

        print(f"\n  {self.ad} - Randevu Gecmisi "
              f"(Toplam: {len(self.randevular)} | "
              f"Aktif: {len(aktif)} | Iptal: {len(iptal)})")

        if not self.randevular:
            print("  Henuz randevu bulunmuyor.")
            return

        for r in self.randevular:
            r.randevu_bilgisi()

    def __str__(self):
        return (f"Hasta [{self.hasta_id}] | Ad: {self.ad} | "
                f"TC: {self.tc} | Tel: {self.telefon} | Yas: {self.yas}")



#  DOKTOR SINIFI


class Doktor:
    def __init__(self, doktor_id, ad, uzmanlik, uygun_saatler):
        self.doktor_id     = doktor_id
        self.ad            = ad
        self.uzmanlik      = uzmanlik
        self.uygun_saatler = sorted(uygun_saatler)  # Sirali tutar
        self.puanlar       = []                      # Hasta puanları

    def uygunluk_kontrol(self, saat):
        """Verilen saatin musait olup olmadigini kontrol eder."""
        return saat in self.uygun_saatler

    def saati_kaldir(self, saat):
        """Randevu alindiginda o saati musait listesinden cikarir."""
        if saat in self.uygun_saatler:
            self.uygun_saatler.remove(saat)

    def saati_ekle(self, saat):
        """Randevu iptal edildiginde saati geri ekler (sirali)."""
        if saat not in self.uygun_saatler:
            self.uygun_saatler.append(saat)
            self.uygun_saatler.sort()

    def puan_ver(self, puan):
        """Hastadan gelen puani kaydeder (1-5 arasi). """
        if 1 <= puan <= 5:
            self.puanlar.append(puan)
            print(f"  Dr. {self.ad} icin {puan}/5 puan kaydedildi.")
        else:
            print("  Gecersiz puan! 1 ile 5 arasinda bir deger girin.")

    def ortalama_puan(self):
        """Doktorun ortalama puanini dondurur."""
        if not self.puanlar:
            return "Puan yok"
        return f"{sum(self.puanlar)/len(self.puanlar):.1f}/5 ({len(self.puanlar)} oy)"

    def __str__(self):
        saatler = ", ".join(self.uygun_saatler) if self.uygun_saatler else "Musait saat yok"
        return (f"Dr. {self.ad} | Uzmanlik: {self.uzmanlik} | "
                f"Musait: {saatler} | Puan: {self.ortalama_puan()}")



#  RANDEVU SINIFI


class Randevu:
    def __init__(self, randevu_id, tarih, saat, doktor, hasta, sikayet=""):
        self.randevu_id = randevu_id
        self.tarih      = tarih
        self.saat       = saat
        self.doktor     = doktor
        self.hasta      = hasta
        self.sikayet    = sikayet       # Hasta sikayeti
        self.durum      = "Aktif"

    def randevu_olustur(self):
        """Randevuyu aktif hale getirir; doktoru ve hastayı gunceller."""
        self.durum = "Aktif"
        self.doktor.saati_kaldir(self.saat)
        self.hasta.randevu_al(self)
        print(f"  [OK] {self.hasta.ad} icin randevu olusturuldu. ID: {self.randevu_id}")

    def randevu_iptal(self):
        """Randevuyu iptal eder ve doktora saati geri verir."""
        if self.durum == "Iptal":
            print("  Bu randevu zaten iptal edilmis.")
            return
        self.durum = "Iptal"
        self.doktor.saati_ekle(self.saat)
        print(f"  Randevu [{self.randevu_id}] iptal edildi. "
              f"Saat {self.saat} tekrar musait.")

    def randevu_bilgisi(self):
        """Randevu detaylarini ekrana yazdirir."""
        sikayet_str = f" | Sikayet: {self.sikayet}" if self.sikayet else ""
        durum_str   = "[AKTIF]" if self.durum == "Aktif" else "[IPTAL]"
        print(f"  {durum_str} [{self.randevu_id}] {self.tarih} {self.saat} | "
              f"Dr. {self.doktor.ad} ({self.doktor.uzmanlik}) | "
              f"Hasta: {self.hasta.ad}{sikayet_str}")

    def __str__(self):
        return (f"Randevu {self.randevu_id} | "
                f"{self.tarih} {self.saat} | "
                f"{self.hasta.ad} -> Dr. {self.doktor.ad} | {self.durum}")




#  SISTEM SINIFI


class RandevuSistemi:
    def __init__(self):
        self.hastalar        = {}   # {hasta_id: Hasta}
        self.doktorlar       = {}   # {doktor_id: Doktor}
        self.randevular      = {}   # {randevu_id: Randevu}
        self._hasta_sayaci   = 1    # H001, H002 ...
        self._doktor_sayaci  = 1    # D001, D002 ...
        self._randevu_sayaci = 1    # R001, R002 ...

    #    KAYIT ISLEMLERI 
    
    

    def hasta_kaydet(self, ad, tc, telefon, yas):
        """Sisteme yeni hasta ekler. TC dogrulamasi ve tekrar kayit kontrolu yapar."""
        if not tc_dogrula(tc):
            print("  Gecersiz TC kimlik no! 11 haneli sayi olmali.")
            return None
        for h in self.hastalar.values():
            if h.tc == tc:
                print(f"  Bu TC ile kayitli hasta zaten var: {h.ad} [{h.hasta_id}]")
                return None
        hid   = f"H{self._hasta_sayaci:03d}"
        self._hasta_sayaci += 1
        hasta = Hasta(hid, ad, tc, telefon, yas)
        self.hastalar[hid] = hasta
        print(f"  Hasta kaydedildi. ID: {hid}")
        return hasta

    def doktor_ekle(self, ad, uzmanlik, uygun_saatler):
        """Sisteme yeni doktor ekler. Saat formatlari dogrulanir."""
        gecersiz = [s for s in uygun_saatler if not saat_dogrula(s)]
        if gecersiz:
            print(f"  Gecersiz saat formati: {gecersiz}. HH:MM olmali.")
            return None
        did    = f"D{self._doktor_sayaci:03d}"
        self._doktor_sayaci += 1
        doktor = Doktor(did, ad, uzmanlik, uygun_saatler)
        self.doktorlar[did] = doktor
        print(f"  Doktor eklendi. ID: {did}")
        return doktor

    #      RANDEVU ISLEMLERI

    def randevu_olustur(self, hasta_id, doktor_id, tarih, saat, sikayet=""):
        """
        Hasta, doktor ve saat kontrolu yaparak randevu olusturur.
        Ayni hastanin ayni gune birden fazla randevusu engellenir.
        """
        hasta  = self.hastalar.get(hasta_id)
        doktor = self.doktorlar.get(doktor_id)

        if not hasta:
            print(f"  Hasta bulunamadi: {hasta_id}")
            return None
        if not doktor:
            print(f"  Doktor bulunamadi: {doktor_id}")
            return None
        if not tarih_dogrula(tarih):
            print("  Gecersiz tarih formati! GG.AA.YYYY olmali.")
            return None
        if not saat_dogrula(saat):
            print("  Gecersiz saat formati! HH:MM olmali.")
            return None
        if not doktor.uygunluk_kontrol(saat):
            print(f"  Dr. {doktor.ad} bu saatte musait degil.")
            if doktor.uygun_saatler:
                print(f"  Musait saatler: {', '.join(doktor.uygun_saatler)}")
            else:
                print("  Bugun icin musait saat kalmadi.")
            return None

        # Ayni hastanin ayni gune cift randevu engeli
        for r in self.randevular.values():
            if (r.hasta.hasta_id == hasta_id and
                    r.tarih == tarih and r.durum == "Aktif"):
                print(f"  {hasta.ad} adli hastanin {tarih} tarihinde "
                      f"zaten aktif randevusu var (ID: {r.randevu_id}).")
                return None

        rid     = f"R{self._randevu_sayaci:03d}"
        self._randevu_sayaci += 1
        randevu = Randevu(rid, tarih, saat, doktor, hasta, sikayet)
        randevu.randevu_olustur()
        self.randevular[rid] = randevu
        return randevu

    def randevu_iptal(self, randevu_id):
        """Randevu ID'sine gore iptali gerceklestirir."""
        randevu = self.randevular.get(randevu_id)
        if randevu:
            randevu.randevu_iptal()
        else:
            print(f"  Randevu bulunamadi: {randevu_id}")

    #     GORUNTULEME / RAPORLAR 

    def gunluk_randevu_listesi(self, tarih, doktor_id=None):
        """
        Belirtilen tarihe ait aktif randevulari listeler.
        Istege bagli olarak belirli bir doktora gore filtreler.
        """
        if not tarih_dogrula(tarih):
            print("  Gecersiz tarih formati! GG.AA.YYYY olmali.")
            return

        liste = [r for r in self.randevular.values()
                 if r.tarih == tarih and r.durum == "Aktif"]

        if doktor_id:
            doktor = self.doktorlar.get(doktor_id)
            if not doktor:
                print(f"  Doktor bulunamadi: {doktor_id}")
                return
            liste  = [r for r in liste if r.doktor.doktor_id == doktor_id]
            baslik = f"Dr. {doktor.ad} - {tarih} Randevulari"
        else:
            baslik = f"{tarih} Tarihli Tum Randevular"

        print(f"\n  {baslik} ({len(liste)} adet):")
        if not liste:
            print("  Bu kriterlere uygun aktif randevu yok.")
            return
        for r in sorted(liste, key=lambda x: x.saat):
            r.randevu_bilgisi()

    def tum_doktorlar(self):
        """Sistemdeki tum doktorlari listeler."""
        if not self.doktorlar:
            print("  Sistemde kayitli doktor yok.")
            return
        print("\n  --- Doktor Listesi ---")
        for d in self.doktorlar.values():
            print(f"  [{d.doktor_id}] {d}")

    def tum_hastalar(self):
        """Sistemdeki tum hastalari listeler."""
        if not self.hastalar:
            print("  Sistemde kayitli hasta yok.")
            return
        print("\n  --- Hasta Listesi ---")
        for h in self.hastalar.values():
            print(f"  {h}")

    def doktora_puan_ver(self, doktor_id, puan):
        """Doktora puan verir."""
        doktor = self.doktorlar.get(doktor_id)
        if doktor:
            doktor.puan_ver(puan)
        else:
            print(f"  Doktor bulunamadi: {doktor_id}")

# DEMO VERILERI



def demo_yukle(sistem):
    """Sistemi ornek veri ile baslatir."""
    print("\n  Demo verileri yukleniyor...")
    sistem.doktor_ekle("Selin Yılmaz", "Kardiyoloji",
                       ["09:00", "10:00", "11:00", "14:00", "15:00"])
    sistem.doktor_ekle("Mert Demir",    "Göz Hastalıkları",
                       ["08:30", "09:30", "13:00", "16:00"])
    sistem.doktor_ekle("Burak Kaya",  "Nöroloji",
                       ["10:00", "11:30", "14:30", "15:30"])
 
    sistem.hasta_kaydet("Ali Celik",    "12345678901", "0532-111-2233", 35)
    sistem.hasta_kaydet("Zeynep Çetin", "98765432100", "0543-444-5566", 28)
    sistem.hasta_kaydet("Ömer Yılmaz",   "11122233344", "0555-777-8899", 52)
 
    # Ornek randevular
    sistem.randevu_olustur("H001", "D001", "25.04.2026", "09:00", "Göğüs ağrısı")
    sistem.randevu_olustur("H002", "D002", "25.04.2026", "08:30", "Göz kızarıklığı")

    print("  " + "-" * 48)
 
 

#  KONSOL MENUSU


def menu():
    sistem = RandevuSistemi()
 
    print("\n" + "=" * 52)
    print("      Online Doktor Randevu Sistemi")
    print("=" * 52)
 
    demo_yukle(sistem)
 
    while True:
        print("\n" + "=" * 52)
        print("  ANA MENU")
        print("  1. Hasta Kayit")
        print("  2. Randevu Al")
        print("  3. Randevu Iptal Et")
        print("  4. Gunluk Randevu Listesi")
        print("  5. Doktora Gore Randevu Listesi")
        print("  6. Hasta Randevu Gecmisi")
        print("  7. Tum Doktorlari Listele")
        print("  8. Tum Hastalari Listele")
        print("  9. Doktora Puan Ver")
        print("  0. Cikis")
        print("=" * 52)
 
        secim = input("  Seciminiz: ").strip()
 
        # ── 1. HASTA KAYIT ──────────────────────────────
        if secim == "1":
            print("\n  -- Hasta Kayit --")
            ad  = input("  Ad Soyad : ").strip()
            tc  = input("  TC No    : ").strip()
            tel = input("  Telefon  : ").strip()
            yas = int_al("  Yas      : ", min_val=0, max_val=122)
            if yas is None:
                continue
            sistem.hasta_kaydet(ad, tc, tel, yas)
 
        # ── 2. RANDEVU AL ───────────────────────────────
        elif secim == "2":
            sistem.tum_hastalar()
            hasta_id = input("\n  Hasta ID            : ").strip().upper()
 
            sistem.tum_doktorlar()
            doktor_id = input("\n  Doktor ID           : ").strip().upper()
 
            doktor = sistem.doktorlar.get(doktor_id)
            if doktor:
                msaatler = ", ".join(doktor.uygun_saatler) or "Musait saat yok"
                print(f"  Musait Saatler: {msaatler}")
 
            tarih   = input("  Tarih (GG.AA.YYYY)  : ").strip()
            saat    = input("  Saat  (HH:MM)       : ").strip()
            sikayet = input("  Sikayet (opsiyonel) : ").strip()
            sistem.randevu_olustur(hasta_id, doktor_id, tarih, saat, sikayet)
 
        # ── 3. RANDEVU IPTAL ────────────────────────────
        elif secim == "3":
            rid = input("\n  Randevu ID : ").strip().upper()
            sistem.randevu_iptal(rid)
 
        # ── 4. GUNLUK LISTE ─────────────────────────────
        elif secim == "4":
            tarih = input("\n  Tarih (GG.AA.YYYY): ").strip()
            sistem.gunluk_randevu_listesi(tarih)
 
        # ── 5. DOKTORA GORE LISTE ───────────────────────
        elif secim == "5":
            sistem.tum_doktorlar()
            doktor_id = input("\n  Doktor ID           : ").strip().upper()
            tarih     = input("  Tarih (GG.AA.YYYY)  : ").strip()
            sistem.gunluk_randevu_listesi(tarih, doktor_id)
 
        # ── 6. HASTA GECMISI ────────────────────────────
        elif secim == "6":
            sistem.tum_hastalar()
            hid   = input("\n  Hasta ID : ").strip().upper()
            hasta = sistem.hastalar.get(hid)
            if hasta:
                hasta.randevu_gecmisi()
            else:
                print(f"  Hasta bulunamadi: {hid}")
 
        # ── 7. DOKTOR LISTESI ───────────────────────────
        elif secim == "7":
            sistem.tum_doktorlar()
 
        # ── 8. HASTA LISTESI ────────────────────────────
        elif secim == "8":
            sistem.tum_hastalar()
 
        # ── 9. DOKTORA PUAN VER ─────────────────────────
        elif secim == "9":
            sistem.tum_doktorlar()
            did  = input("\n  Doktor ID   : ").strip().upper()
            puan = int_al("  Puan (1-5)  : ", min_val=1, max_val=5)
            if puan is None:
                continue
            sistem.doktora_puan_ver(did, puan)
 
        # ── CIKIS ───────────────────────────────────────
        elif secim == "0":
            print("\n  Gule gule!\n")
            break
 
        else:
            print("  Gecersiz secim, tekrar deneyin.")
 

#  BASLANGIC

if __name__ == "__main__":
    menu()
 