# 🏥 Online Doktor Randevu Sistemi

Konsol tabanlı, nesne yönelimli programlama (OOP) mantığıyla Python'da geliştirilmiş bir klinik randevu yönetim sistemidir. Bu proje; hasta kaydı, doktor yönetimi, randevu oluşturma/iptali ve doktor değerlendirme süreçlerini dijital ortamda simüle etmek için tasarlanmıştır.

## ✨ Özellikler

* **Hasta ve Doktor Yönetimi:** Sisteme yeni hasta ve doktor ekleme, listeleme.
* **Akıllı Randevu Akışı:** Doktorların müsaitlik durumuna göre randevu oluşturma ve iptal edildiğinde saati tekrar boşa çıkarma.
* **Gelişmiş Veri Doğrulamaları:**
  * 11 haneli geçerli TC Kimlik numarası kontrolü.
  * Saat (`HH:MM`) ve Tarih (`GG.AA.YYYY`) formatı doğrulaması.
  * Aynı hastanın aynı güne birden fazla randevu almasının engellenmesi.
  * Aynı TC kimlik numarasıyla çift hasta kaydının engellenmesi.
* **Doktor Değerlendirme:** Hastaların doktorlara hizmet sonrası 1-5 arası puan verebilmesi ve ortalama puan hesaplaması.
* **Filtreleme ve Raporlama:** Belirli bir tarihe veya doktora göre günlük aktif randevuları listeleme, hastaya özel randevu geçmişi görüntüleme.

## 🚀 Kurulum ve Kullanım

### Gereksinimler
* Python 3.x

### Çalıştırma
Projeyi bilgisayarınıza klonladıktan veya indirdikten sonra, terminal/komut satırında dosyanın bulunduğu dizine gidin ve aşağıdaki komutu çalıştırın:

```bash
python randevusistemi.py

Not: Sistem başlatıldığında özellikleri hızlıca test edebilmeniz için bazı demo verileri (örnek doktorlar, hastalar ve randevular) otomatik olarak yüklenecektir.

📋 Menü Kullanım Rehberi
Program çalıştığında karşınıza çıkan ana menü üzerinden numaraları tuşlayarak tüm işlemleri yönetebilirsiniz:

Hasta Kayıt: Sisteme yeni hasta ekler. (Ad, geçerli bir TC, Telefon ve Yaş istenir).

Randevu Al: Kayıtlı bir hasta için, seçilen doktorun müsait saatlerinden birine randevu oluşturur.

Randevu İptal Et: R001 vb. formatındaki ID ile aktif randevuyu iptal eder; ilgili saat doktorun müsait saatlerine geri döner.

Günlük Randevu Listesi: Belirtilen tarihteki tüm aktif randevuları saat sırasına göre listeler.

Doktora Göre Randevu Listesi: Belirli bir tarihte, sadece seçilen doktorun güncel randevularını filtreler.

Hasta Randevu Geçmişi: İlgili hastanın aldığı tüm aktif ve iptal edilmiş randevularının özetini gösterir.

Tüm Doktorları Listele: Doktorların uzmanlıklarını, güncel müsait saatlerini ve ortalama puanlarını gösterir.

Tüm Hastaları Listele: Kayıtlı hastaların kimlik ve iletişim bilgilerini listeler.

Doktora Puan Ver: Belirli bir doktora 1 ile 5 arasında tam sayı olarak puan verilmesini sağlar.

Çıkış: Programı sonlandırır. (Veriler geçici bellekte tutulduğu için program kapatıldığında kayıtlar sıfırlanır).

🏗️ Proje Yapısı (Sınıflar)
Proje, temiz ve modüler bir yapıda tutulması için 4 temel sınıf etrafında kurgulanmıştır:

Hasta: Hasta kimlik bilgilerini ve kişisel randevu geçmişini (aktif/iptal) tutar.

Doktor: Doktorun uzmanlık bilgilerini, esnek/dinamik müsait saat listesini ve hasta puanlarını yönetir.

Randevu: Randevu durumunu, tarih/saat verisini ve hasta şikayetlerini kapsar.

RandevuSistemi: Tüm objeleri (dict yapılarında) barındıran, validasyonları kontrol eden ve konsol akışını yöneten ana kontrolcü (Controller) sınıftır.
