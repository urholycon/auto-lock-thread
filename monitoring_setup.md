# 🔍 Bot Monitoring Setup Guide

Panduan lengkap untuk setup monitoring otomatis agar Discord bot Anda tetap hidup 24/7.

## 🚀 Quick Setup URLs

Setelah bot Anda deploy, gunakan URL berikut untuk monitoring:

- **Ping URL**: `https://your-replit-url.replit.app/ping`
- **Status URL**: `https://your-replit-url.replit.app/status`
- **Health Check**: `https://your-replit-url.replit.app/health`
- **Uptime Stats**: `https://your-replit-url.replit.app/uptime`

## 📊 External Monitoring Services

### 1. UptimeRobot (Free & Recommended)

**Setup Steps:**
1. Buka [https://uptimerobot.com](https://uptimerobot.com)
2. Daftar akun gratis
3. Klik "Add New Monitor"
4. Pilih "HTTP(s)" sebagai Monitor Type
5. Masukkan URL bot: `https://your-replit-url.replit.app/ping`
6. Set monitoring interval: 5 minutes
7. Klik "Create Monitor"

**Keuntungan:**
- ✅ Gratis sampai 50 monitor
- ✅ Ping setiap 5 menit
- ✅ Email alert saat bot down
- ✅ Status page publik

### 2. Pingdom (Free Trial)

**Setup Steps:**
1. Buka [https://www.pingdom.com](https://www.pingdom.com)
2. Start free trial
3. Add new check
4. URL to check: `https://your-replit-url.replit.app/ping`
5. Check interval: 5 minutes

### 3. StatusCake (Free Plan)

**Setup Steps:**
1. Buka [https://www.statuscake.com](https://www.statuscake.com)
2. Create free account
3. Add new uptime test
4. Website URL: `https://your-replit-url.replit.app/health`
5. Test interval: 5 minutes

## 🛠️ Built-in Monitor (Bonus)

Bot sudah dilengkapi dengan internal monitor yang bisa dijalankan secara terpisah:

```bash
# Jalankan internal monitor
python monitor.py --url https://your-bot-url.replit.app --interval 300

# Custom interval (dalam detik)
python monitor.py --url https://your-bot-url.replit.app --interval 120
```

## 🔧 Advanced Monitoring Setup

### Multi-Service Strategy (Recommended)

Gunakan beberapa service monitoring untuk redundancy:

1. **Primary**: UptimeRobot (setiap 5 menit)
2. **Secondary**: StatusCake (setiap 10 menit)
3. **Internal**: Built-in monitor (setiap 5 menit)

### Custom Webhook Alerts

Tambahkan webhook alerts ke Discord untuk notifikasi real-time:

```python
# Contoh webhook setup (opsional)
webhook_url = "YOUR_DISCORD_WEBHOOK_URL"

# Setup di UptimeRobot:
# 1. Pilih monitor Anda
# 2. Klik "Alert Contacts"
# 3. Add webhook dengan URL Discord webhook Anda
```

## 📈 Monitoring Endpoints

Bot menyediakan beberapa endpoint untuk monitoring:

| Endpoint | Purpose | Response |
|----------|---------|----------|
| `/ping` | Basic alive check | `{"response": "pong", "status": "alive"}` |
| `/status` | Bot status info | Full bot information |
| `/health` | Health check | `{"health": "ok"}` |
| `/uptime` | Detailed statistics | Uptime stats and metrics |

## 🔍 Troubleshooting

### Bot Sering Sleep?

1. **Check ping frequency**: Pastikan monitoring ping setiap 5 menit
2. **Multiple monitors**: Gunakan 2-3 service monitoring berbeda
3. **Endpoint variety**: Ping berbeda endpoint secara bergantian

### Monitor Tidak Bekerja?

1. **Test URL manually**: Buka URL di browser, pastikan respond
2. **Check response time**: Pastikan response < 30 detik
3. **Verify HTTPS**: Pastikan menggunakan HTTPS, bukan HTTP

### Performance Issues?

1. **Reduce ping frequency**: Jangan terlalu sering (minimal 2-3 menit)
2. **Use lightweight endpoints**: `/ping` lebih ringan dari `/status`
3. **Monitor statistics**: Check `/uptime` untuk melihat beban ping

## 🎯 Best Practices

1. **Interval Timing**: 5 menit optimal (tidak terlalu cepat/lambat)
2. **Multiple Monitors**: 2-3 service berbeda untuk redundancy
3. **Alert Setup**: Aktifkan email/Discord notification
4. **Regular Checks**: Monitor dashboard mingguan
5. **Backup Strategy**: Selalu ada rencana cadangan jika monitor gagal

## 📱 Mobile Monitoring

### UptimeRobot App
- Download app untuk iOS/Android
- Real-time notifications
- Quick status overview

### Custom Discord Bot
Buat bot khusus monitoring yang ping bot utama dan kirim alert ke Discord channel Anda.

---

**💡 Pro Tip**: Kombinasikan external monitoring (UptimeRobot) dengan internal monitor untuk monitoring terbaik. Bot akan tetap hidup 24/7 tanpa perlu intervensi manual!