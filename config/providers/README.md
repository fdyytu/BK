# PPOB Provider Integration System

Sistem integrasi provider untuk platform PPOB yang mengimplementasikan prinsip SOLID dan DRY.

## Struktur
config/providers/
├── __init__.py
├── README.md               # Dokumentasi providers
├── core/                  # Core provider functionality
│   ├── __init__.py
│   ├── base.py           # Base provider class
│   ├── interfaces.py     # Provider interfaces
│   ├── exceptions.py     # Custom exceptions
│   └── validators.py     # Data validators
│
├── payment/              # Payment providers (existing)
│   ├── __init__.py
│   ├── bank/            # Bank transfer providers
│   │   ├── __init__.py
│   │   ├── bca.py
│   │   ├── mandiri.py
│   │   └── bni.py
│   ├── ewallet/         # E-wallet providers 
│   │   ├── __init__.py
│   │   ├── ovo.py
│   │   ├── dana.py
│   │   └── gopay.py
│   └── gateway/         # Payment gateway
│       ├── __init__.py
│       ├── midtrans.py
│       └── xendit.py
│
├── telco/               # Telco providers (NEW)
│   ├── __init__.py
│   ├── pulsa/          # Pulsa providers
│   │   ├── __init__.py
│   │   ├── mobilepulsa.py
│   │   └── digiflazz.py
│   └── data/           # Data package providers
│       ├── __init__.py
│       ├── mobilepulsa.py
│       └── digiflazz.py
│
├── utilities/           # Utility bill providers (NEW)
│   ├── __init__.py
│   ├── pln/           # Electricity providers
│   │   ├── __init__.py
│   │   ├── prepaid.py
│   │   └── postpaid.py
│   ├── pdam/          # Water providers
│   │   ├── __init__.py
│   │   └── regional.py
│   └── internet/      # Internet providers
│       ├── __init__.py
│       ├── indihome.py
│       └── firstmedia.py
│
├── voucher/            # Voucher providers (NEW)
│   ├── __init__.py
│   ├── games/         # Game vouchers
│   │   ├── __init__.py
│   │   ├── codashop.py
│   │   └── unipin.py
│   └── streaming/     # Streaming vouchers
│       ├── __init__.py
│       ├── netflix.py
│       └── spotify.py
│
├── notification/       # Notification providers (existing)
│   ├── __init__.py
│   ├── sms/          
│   │   ├── __init__.py
│   │   └── twilio.py
│   ├── email/
│   │   ├── __init__.py
│   │   └── sendgrid.py
│   └── push/
│       ├── __init__.py
│       └── firebase.py
│
├── shipping/          # Shipping providers (existing)
│   ├── __init__.py
│   ├── jne.py
│   ├── sicepat.py
│   └── anteraja.py
│
└── settings/         # Provider settings
    ├── __init__.py
    ├── production.py
    ├── staging.py
    └── development.py