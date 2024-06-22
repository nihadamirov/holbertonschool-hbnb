HBnB Evolution Project
holbertonschool-hbnb/
│
├── app/
│   ├── __init__.py             # Ana uygulama başlangıç dosyası
│   ├── models/                 # Model sınıfları
│   │   ├── __init__.py         # Models paketi başlangıç dosyası
│   │   ├── base_model.py       # Temel model sınıfı (BaseModel)
│   │   ├── user.py             # Kullanıcı model sınıfı
│   │   ├── place.py            # Yer model sınıfı
│   │   ├── city.py             # Şehir model sınıfı
│   │   ├── country.py          # Ülke model sınıfı
│   │   ├── amenity.py          # Olanak model sınıfı
│   │   ├── review.py           # İnceleme model sınıfı
│   │   └── ...                 # Diğer model sınıfları
│   ├── api/                    # API uygulama dosyaları
│   │   ├── __init__.py         # API paketi başlangıç dosyası
│   │   ├── v1/                 # API'nin versiyon 1 dosyaları
│   │   │   ├── __init__.py     # v1 paketi başlangıç dosyası
│   │   │   ├── users.py        # Kullanıcılarla ilgili API işlemleri
│   │   │   ├── places.py       # Yerlerle ilgili API işlemleri
│   │   │   ├── cities.py       # Şehirlerle ilgili API işlemleri
│   │   │   ├── countries.py    # Ülkelerle ilgili API işlemleri
│   │   │   ├── amenities.py    # Olanaklarla ilgili API işlemleri
│   │   │   ├── reviews.py      # İncelemelerle ilgili API işlemleri
│   │   │   └── ...             # Diğer API işlemleri dosyaları
│   ├── database/               # Veritabanı yapılandırma dosyaları ve modelleri
│   │   ├── __init__.py         # Veritabanı paketi başlangıç dosyası
│   │   ├── config.py           # Veritabanı yapılandırma dosyası
│   │   ├── models.py           # Veritabanı model sınıfları
│   │   └── ...                 # Diğer veritabanı yardımcı dosyaları
│   ├── utils/                  # Yardımcı işlev ve validasyon dosyaları
│   │   ├── __init__.py         # Yardımcı paketi başlangıç dosyası
│   │   ├── validators.py       # Veri doğrulama işlevleri
│   │   └── ...                 # Diğer yardımcı dosyalar
│   ├── main.py                 # Ana uygulama başlangıç noktası
│   └── ...                     # Diğer uygulama dosyaları
│
├── migrations/                 # Veritabanı migrasyon dosyaları
│   ├── ...                     # Migrasyon dosyaları
│
├── tests/                      # Test dosyaları
│   ├── __init__.py             # Test paketi başlangıç dosyası
│   ├── test_users.py           # Kullanıcı modeli testleri
│   ├── test_places.py          # Yer modeli testleri
│   ├── test_cities.py          # Şehir modeli testleri
│   ├── test_countries.py       # Ülke modeli testleri
│   ├── test_amenities.py       # Olanak modeli testleri
│   ├── test_reviews.py         # İnceleme modeli testleri
│   └── ...                     # Diğer test dosyaları
│
├── Dockerfile                  # Docker konteyner dosyası
├── requirements.txt            # Proje bağımlılıkları
└── ...                         # Diğer proje düzeni dosyaları
