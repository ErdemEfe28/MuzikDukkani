import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Enstruman:
    def __init__(self, ad, stok):
        self.ad = ad
        self.stok = stok

    def satis_yap(self, miktar):
        if miktar <= self.stok:
            self.stok -= miktar
            return True
        else:
            return False

class Musteri:
    def __init__(self, ad):
        self.ad = ad
        self.siparisler = []

class Satis:
    def __init__(self, musteri, enstruman, miktar):
        self.musteri = musteri
        self.enstruman = enstruman
        self.miktar = miktar
        self.tarih = datetime.now()

class Destek:
    def __init__(self, musteri, konu, detay):
        self.musteri = musteri
        self.konu = konu
        self.detay = detay
        self.tarih = datetime.now()

class MuzikDukkaniApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Müzik Enstrümanı Dükkanı Yönetimi")

        self.enstrumanlar = []
        self.musteriler = []
        self.satislar = []
        self.destekler = []

        tk.Label(root, text="Enstrüman Adı:").grid(row=0, column=0)
        self.entry_enstruman_ad = tk.Entry(root)
        self.entry_enstruman_ad.grid(row=0, column=1)

        tk.Label(root, text="Stok Miktarı:").grid(row=1, column=0)
        self.entry_stok = tk.Entry(root)
        self.entry_stok.grid(row=1, column=1)

        tk.Button(root, text="Enstrüman Ekle", command=self.enstruman_ekle).grid(row=2, column=0, columnspan=2)

        self.listbox_enstrumanlar = tk.Listbox(root, width=50)
        self.listbox_enstrumanlar.grid(row=3, column=0, columnspan=2)

        tk.Label(root, text="Müşteri Adı:").grid(row=4, column=0)
        self.entry_musteri_ad = tk.Entry(root)
        self.entry_musteri_ad.grid(row=4, column=1)

        tk.Label(root, text="Satış Miktarı:").grid(row=5, column=0)
        self.entry_satis_miktar = tk.Entry(root)
        self.entry_satis_miktar.grid(row=5, column=1)

        tk.Button(root, text="Satış Yap", command=self.satis_yap).grid(row=6, column=0, columnspan=2)

        tk.Label(root, text="Destek Konusu:").grid(row=7, column=0)
        self.entry_destek_konu = tk.Entry(root)
        self.entry_destek_konu.grid(row=7, column=1)

        tk.Label(root, text="Destek Detayı:").grid(row=8, column=0)
        self.entry_destek_detay = tk.Entry(root)
        self.entry_destek_detay.grid(row=8, column=1)

        tk.Button(root, text="Destek Talebi Oluştur", command=self.destek_talebi_olustur).grid(row=9, column=0, columnspan=2)

        tk.Button(root, text="Raporları Görüntüle", command=self.raporlari_goster).grid(row=10, column=0, columnspan=2)

        self.listbox_rapor = tk.Listbox(root, width=80)
        self.listbox_rapor.grid(row=11, column=0, columnspan=2)

    def enstruman_ekle(self):
        ad = self.entry_enstruman_ad.get()
        try:
            stok = int(self.entry_stok.get())
            yeni = Enstruman(ad, stok)
            self.enstrumanlar.append(yeni)
            self.listbox_enstrumanlar.insert(tk.END, f"{ad} - Stok: {stok}")
            messagebox.showinfo("Başarılı", "Enstrüman eklendi.")
        except ValueError:
            messagebox.showerror("Hata", "Stok miktarı bir sayı olmalıdır.")

    def satis_yap(self):
        secili_index = self.listbox_enstrumanlar.curselection()
        if not secili_index:
            messagebox.showerror("Hata", "Bir enstrüman seçin.")
            return
        try:
            miktar = int(self.entry_satis_miktar.get())
            enstruman = self.enstrumanlar[secili_index[0]]
            if enstruman.satis_yap(miktar):
                musteri_ad = self.entry_musteri_ad.get()
                musteri = next((m for m in self.musteriler if m.ad == musteri_ad), None)
                if not musteri:
                    musteri = Musteri(musteri_ad)
                    self.musteriler.append(musteri)
                satis = Satis(musteri, enstruman, miktar)
                musteri.siparisler.append(satis)
                self.satislar.append(satis)
                self.listbox_enstrumanlar.delete(secili_index)
                self.listbox_enstrumanlar.insert(secili_index, f"{enstruman.ad} - Stok: {enstruman.stok}")
                messagebox.showinfo("Başarılı", "Satış yapıldı.")
            else:
                messagebox.showerror("Hata", "Yetersiz stok.")
        except ValueError:
            messagebox.showerror("Hata", "Satış miktarı bir sayı olmalıdır.")

    def destek_talebi_olustur(self):
        musteri_ad = self.entry_musteri_ad.get()
        konu = self.entry_destek_konu.get()
        detay = self.entry_destek_detay.get()
        if not (musteri_ad and konu and detay):
            messagebox.showerror("Hata", "Tüm destek bilgilerini doldurun.")
            return
        musteri = next((m for m in self.musteriler if m.ad == musteri_ad), None)
        if not musteri:
            musteri = Musteri(musteri_ad)
            self.musteriler.append(musteri)
        destek = Destek(musteri, konu, detay)
        self.destekler.append(destek)
        messagebox.showinfo("Başarılı", "Destek talebi oluşturuldu.")

    def raporlari_goster(self):
        self.listbox_rapor.delete(0, tk.END)
        self.listbox_rapor.insert(tk.END, "Satışlar:")
        for satis in self.satislar:
            self.listbox_rapor.insert(tk.END, f"{satis.tarih.strftime('%d/%m/%Y %H:%M')} - {satis.musteri.ad} - {satis.enstruman.ad} x{satis.miktar}")
        self.listbox_rapor.insert(tk.END, "")
        self.listbox_rapor.insert(tk.END, "Destek Talepleri:")
        for destek in self.destekler:
            self.listbox_rapor.insert(tk.END, f"{destek.tarih.strftime('%d/%m/%Y %H:%M')} - {destek.musteri.ad} - {destek.konu} - {destek.detay}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MuzikDukkaniApp(root)
    root.mainloop()
