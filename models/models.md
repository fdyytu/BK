# Models Directory

Direktori `models/` ini berisi seluruh struktur model, interface, dan value object untuk aplikasi marketplace dan layanan digital, dengan arsitektur yang terinspirasi Domain-Driven Design (DDD). Struktur ini memungkinkan skalabilitas, maintainabilitas, serta pemisahan domain yang jelas.

---



### Penjelasan Tiap Folder

#### 1. **abstracts/**
Berisi abstraksi dasar dan perilaku umum:
- **base/**: Model, entity, dan aggregate root dasar.
- **products/**: Abstraksi produk (produk digital, fisik, jasa).
- **transactions/**: Abstraksi transaksi, pembayaran, dan refund.

#### 2. **interfaces/**
Berisi interface (abstract base class) untuk kontrak perilaku:
- **payment/**: Interface pembayaran, validasi, kalkulasi.
- **tracking/**: Interface tracking status dan riwayat.
- **notification/**: Interface notifikasi dan pengirimannya.

#### 3. **users/**
Struktur model user berdasarkan peran:
- **base/**: Entity & status user umum.
- **owner/**, **admin/**, **seller/**, **buyer/**: Model, permission, settings, dan atribut spesifik tiap peran.

#### 4. **core/**
Fitur fundamental aplikasi:
- **authentication/**: Kredensial, session, token, 2FA.
- **access/**: Role, permission, policy.
- **wallet/**: Entity & value object terkait dompet.

#### 5. **ppob/**
Domain PPOB (Payment Point Online Bank):
- **payment/**: Bank transfer, e-wallet, virtual account.
- **telco/**: Pulsa, paket data, tagihan telekomunikasi.
- **utility/**: Listrik (PLN), air (PDAM), internet.

#### 6. **digital/**
Produk digital:
- **voucher/**: Voucher game & streaming.
- **subscription/**: Langganan streaming & game.

#### 7. **transaction/**
Transaksi dan dokumen terkait:
- **entities/**: Order, invoice, receipt.
- **value_objects/**: Value object untuk nomor order/invoice, jenis transaksi.
- **aggregates/**: Aggregate root transaksi.

---

## Contoh Penggunaan

Setiap file pada folder ini berisi class Python dengan struktur dan docstring yang jelas, siap untuk di-extend atau diintegrasikan ke dalam service/bisnis logic aplikasi Anda.

Contoh menginisialisasi produk digital:
```python
from models.abstracts.products.digital_product import DigitalProduct

product = DigitalProduct(name="Ebook Premium", price=50000, download_url="https://...")
```

Contoh interface:
```python
from models.interfaces.payment.payable import Payable

class MyInvoice(Payable):
    def get_amount(self):
        return 150000
```

---

## Standar & Best Practice

- **Domain-Driven Design (DDD):** Pemisahan domain, aggregate root, entity, value objects, dan event (bisa ditambahkan jika dibutuhkan).
- **Interface Segregation:** Gunakan interface agar mudah extend dan testable.
- **Scalable Structure:** Mudah dikembangkan untuk domain/fitur baru.

---

## Kontribusi

1. **Ikuti struktur folder dan penamaan.**
2. **Tambahkan docstring dan type hint pada setiap class/method.**
3. **Pisahkan logic domain dengan infrastructure/framework.**
4. **Tambahkan unit test untuk setiap komponen baru.**

---

## Lisensi

MIT License