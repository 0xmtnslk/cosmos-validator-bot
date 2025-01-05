# 1. Yeni dizin oluştur

```
mkdir cosmos-validator-bot
cd cosmos-validator-bot
```

# 4. setup.sh'ı çalıştırılabilir yap
```
chmod +x setup.sh
```
# 5. Kurulumu başlat
```
./setup.sh
```
# 6. İzinleri düzenleyelim.

### Tüm dizin yapısının izinlerini düzelt
```
sudo chown -R tenderduty:tenderduty /root/cosmos-validator-bot
sudo chmod -R 755 /root/cosmos-validator-bot
```
### Config dosyasının izinlerini özel olarak ayarla
```
sudo chmod 644 /root/cosmos-validator-bot/tenderduty/config.yml
```
```
sudo chmod 755 /root
```
# 8. Botu başlat
```
python3 bot.py
```

# 9. Tenderduty servisini başlat

#### Systemd'yi yeniden yükle
```
sudo systemctl daemon-reload
```
#### Servisi yeniden başlat
```
sudo systemctl restart tenderduty
```
#### Durumu kontrol et
```
sudo systemctl status tenderduty
```
##### Logları izle
```
journalctl -u tenderduty -f
```
