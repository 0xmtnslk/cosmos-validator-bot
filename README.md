# 1. Yeni dizin oluştur

```
mkdir cosmos-validator-bot
cd cosmos-validator-bot
```

# 2. Gerekli dosyaları oluştur
```
mkdir tenderduty
touch config.json networks.json bot.py setup.sh
```


# 4. setup.sh'ı çalıştırılabilir yap
```
chmod +x setup.sh
```
# 5. Kurulumu başlat
```
./setup.sh
```
# 6. config.json'a Telegram bot token'ını ekle
# (config.json dosyasını düzenleyip token'ı girin)

# 7. networks.json'ı düzenle
# (İstediğiniz ağları ekleyin/çıkarın)

# 8. Botu başlat
```
python3 bot.py
```

# 9. Tenderduty servisini başlat
```
sudo systemctl start tenderduty
```

