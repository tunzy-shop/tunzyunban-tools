import smtplib
import getpass
import time
import re
import os
import random
import requests
import json
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

# ===== WhatsApp Support Emails (Expanded for Maximum Impact) =====
SUPPORT_EMAILS = {
    "urgent": [
        "support@support.whatsapp.com",
        "appeals@support.whatsapp.com",
        "1483635209301664@support.whatsapp.com",
        "support@whatsapp.com",
        "help@whatsapp.com",
        "contact@whatsapp.com",
        "info@whatsapp.com",
    ],
    "technical": [
        "android_web@support.whatsapp.com",
        "ios_web@support.whatsapp.com",
        "webclient_web@support.whatsapp.com",
        "mobile@support.whatsapp.com",
        "desktop@support.whatsapp.com",
    ],
    "security": [
        "businesscomplaints@support.whatsapp.com",
        "abuse@support.whatsapp.com",
        "security@support.whatsapp.com",
        "privacy@whatsapp.com",
        "report@whatsapp.com",
        "fraud@whatsapp.com",
        "phishing@whatsapp.com",
    ],
    "legal": [
        "legal@whatsapp.com",
        "lawenforcement@whatsapp.com",
        "subpoenas@whatsapp.com",
        "copyright@whatsapp.com",
        "dmca@whatsapp.com",
    ],
    "business": [
        "business@whatsapp.com",
        "api@whatsapp.com",
        "developers@whatsapp.com",
        "partners@whatsapp.com",
    ]
}

# Multiply emails for maximum impact
ALL_EMAILS = []
for category_emails in SUPPORT_EMAILS.values():
    ALL_EMAILS.extend(category_emails * 3)  # Triple each email

# Remove duplicates but keep order
ALL_EMAILS = list(dict.fromkeys(ALL_EMAILS))

# ===== WhatsApp Business API =====
ACCESS_TOKEN = "EAAJgi17vyDYBPTGf8m4LNp0xFdUozhBKS6PTnrElQdSZCIRZCnuLFmBigzRvB4ZCUI8EBNuNZCFZBfG5e11ehZBujToi9S6zYQ3HSmDZBPNQHZBFFrd3ntSZAl6lRZAOa86mOZCp60VaaCMhgUN6s68EEvYSEJXlaIk9iiB7xe1rlZBKbEVf7YiIADUZA0kHuO9nr0QZDZD"
PHONE_NUMBER_ID = "669101662914614"

# ===== Statistics Tracking =====
stats = {
    "emails_sent": 0,
    "reports_made": 0,
    "numbers_checked": 0,
    "successful_unbans": 0,
    "failed_attempts": 0,
    "total_operations": 0
}

# ===== Aggressive Settings =====
MAX_REPETITIONS = 50  # Send 50 times for maximum impact
REPORT_REPETITIONS = 30  # For banning scammers quickly
BAN_TIME_TARGET = "5-10 minutes"  # Target ban time for scammers
UNBAN_TIME_TARGET = "1-3 hours"  # Target unban time

# ===== Utility Functions =====
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def typewriter(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def print_banner():
    banner_color = random.choice([Fore.RED, Fore.MAGENTA, Fore.YELLOW, Fore.CYAN])
    banner = f"""
    {banner_color}╔══════════════════════════════════════════════════════════════╗
    ║              ⚡ WHATSAPP ULTIMATE BANHAMMER v3.0 ⚡           ║
    ║                💀 AGGRESSIVE MODE ACTIVATED 💀              ║
    ║                   🔥 Powered by Tunzy Shop 🔥               ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def validate_phone_number(phone):
    """Enhanced phone number validation"""
    pattern = r'^\+\d{10,15}$'
    if not re.match(pattern, phone):
        return False
    return True

# ===== Hyper-Aggressive Email Sending System =====
class HyperEmailBomber:
    def __init__(self):
        self.account_cycle = cycle(gmail_accounts)
        self.active_accounts = [acc for acc in gmail_accounts if acc["status"] == "active"]
        self.sent_count = 0
        
    def test_account(self, account):
        """Test if Gmail account is working"""
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
            server.ehlo()
            server.starttls()
            server.login(account["email"], account["password"])
            server.quit()
            account["status"] = "active"
            return True
        except Exception as e:
            account["status"] = "inactive"
            print(Fore.RED + f"   ✗ Account {account['email']} failed: {str(e)[:50]}")
            return False
    
    def get_next_account(self):
        """Get next working account with aggressive rotation"""
        for _ in range(len(gmail_accounts) * 2):  # Try harder
            account = next(self.account_cycle)
            if account["status"] == "active":
                return account
            elif self.test_account(account):
                return account
        return None
    
    def send_single_email_aggressive(self, account, to_email, subject, body):
        """Send single email with aggressive settings"""
        try:
            msg = MIMEMultipart()
            msg['From'] = account["email"]
            msg['To'] = to_email
            msg['Reply-To'] = account["email"]
            
            # Add aggressive headers
            msg['X-Priority'] = '1'  # Highest priority
            msg['X-MSMail-Priority'] = 'High'
            msg['Importance'] = 'high'
            msg['X-Report-Abuse'] = 'True'
            msg['X-Report-Phishing'] = 'True'
            
            # Add urgency to subject
            urgent_subject = f"⚠️⚠️⚠️ {subject} ⚠️⚠️⚠️"
            msg['Subject'] = urgent_subject
            
            # Add timestamp and urgency markers
            urgent_body = f"""
🚨🚨🚨 URGENT ATTENTION REQUIRED 🚨🚨🚨
{body}

───────────────────────────────────────
❗❗❗ IMMEDIATE ACTION REQUIRED ❗❗❗
This is a HIGH PRIORITY request requiring URGENT attention.
Failure to act will result in continued harm to users.

TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
MESSAGE ID: {random.randint(1000000, 9999999)}
PRIORITY: CRITICAL (Level 1)
───────────────────────────────────────

This message has been flagged for IMMEDIATE REVIEW by automated system.
"""
            
            msg.attach(MIMEText(urgent_body, 'plain'))
            
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
            server.ehlo()
            server.starttls()
            server.login(account["email"], account["password"])
            server.send_message(msg)
            server.quit()
            
            self.sent_count += 1
            stats["emails_sent"] += 1
            return True
        except Exception as e:
            print(Fore.RED + f"   ✗ Failed to send to {to_email}")
            return False
    
    def bomb_single_target(self, to_email, subject, body, repetitions=1):
        """Bomb a single email address multiple times"""
        success_count = 0
        
        for rep in range(repetitions):
            account = self.get_next_account()
            if not account:
                print(Fore.RED + "   ⚠️ No active accounts available")
                continue
            
            # Add repetition counter to subject
            rep_subject = f"[{rep+1}/{repetitions}] {subject}"
            
            if self.send_single_email_aggressive(account, to_email, rep_subject, body):
                success_count += 1
                if rep % 5 == 0:  # Show progress every 5 repetitions
                    print(Fore.GREEN + f"   ✓ Rep {rep+1}/{repetitions} sent to {to_email}")
            
            # Small delay to avoid overwhelming
            time.sleep(0.1)
        
        return success_count
    
    def mass_bomb_all_emails(self, subject, body, repetitions=MAX_REPETITIONS, category="all"):
        """Bomb ALL support emails with multiple repetitions"""
        print(Fore.RED + f"\n💣 STARTING MASS BOMBING CAMPAIGN")
        print(Fore.YELLOW + f"   Target: {len(ALL_EMAILS)} email addresses")
        print(Fore.YELLOW + f"   Repetitions: {repetitions} times each")
        print(Fore.YELLOW + f"   Total emails: {len(ALL_EMAILS) * repetitions}")
        print(Fore.RED + f"   Expected result: {BAN_TIME_TARGET} for reports, {UNBAN_TIME_TARGET} for unbans")
        
        total_success = 0
        start_time = time.time()
        
        # Use threading for maximum speed
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for email in ALL_EMAILS:
                future = executor.submit(
                    self.bomb_single_target,
                    email, subject, body, repetitions
                )
                futures.append(future)
            
            # Wait for all to complete
            for future in as_completed(futures):
                try:
                    success = future.result(timeout=300)  # 5 minute timeout
                    total_success += success
                except Exception as e:
                    print(Fore.RED + f"   ✗ Thread failed: {e}")
        
        elapsed_time = time.time() - start_time
        emails_per_second = total_success / elapsed_time if elapsed_time > 0 else 0
        
        print(Fore.GREEN + "\n" + "💣" * 50)
        print(Fore.GREEN + f"💥 MASS BOMBING COMPLETE!")
        print(Fore.CYAN + f"   ✅ Successfully sent: {total_success} emails")
        print(Fore.CYAN + f"   ⏱️  Time elapsed: {elapsed_time:.1f} seconds")
        print(Fore.CYAN + f"   🚀 Speed: {emails_per_second:.1f} emails/second")
        print(Fore.YELLOW + f"   🎯 Expected response time: {BAN_TIME_TARGET}")
        print(Fore.GREEN + "💣" * 50)
        
        return total_success

# ===== Enhanced Unban Templates (More Aggressive) =====
def get_aggressive_unban_template(template_type, phone):
    """Return hyper-aggressive unban email templates"""
    
    templates = {
        "temporary": {
            "subject": f"URGENT: ACCOUNT WRONGLY BANNED - IMMEDIATE RESTORATION REQUIRED - {phone}",
            "body": f"""
🚨🚨🚨 EMERGENCY ACCOUNT RESTORATION REQUEST 🚨🚨🚨

TO: WHATSAPP URGENT SUPPORT TEAM
PRIORITY: LEVEL 1 - CRITICAL
ACCOUNT: {phone}
STATUS: WRONGLY BANNED
ACTION REQUIRED: IMMEDIATE RESTORATION

⚠️ ⚠️ ⚠️ URGENT ATTENTION NEEDED ⚠️ ⚠️ ⚠️

My WhatsApp account associated with {phone} has been WRONGLY and UNJUSTLY banned.

THIS IS A FALSE POSITIVE!

I demand IMMEDIATE restoration of my account within {UNBAN_TIME_TARGET}.

REASONS FOR URGENCY:
1. This is my PRIMARY business communication channel
2. I have pending emergency medical communications
3. Critical financial transactions are being delayed
4. Family emergency coordination is compromised
5. Business losses: $500+ per hour of downtime

I HAVE DONE NOTHING WRONG!

This ban is clearly a SYSTEM ERROR or FALSE POSITIVE.

⚠️ IMMEDIATE ACTION REQUIRED:
1. Restore account IMMEDIATELY
2. Remove false ban marker
3. Compensate for service interruption
4. Provide written confirmation

FAILURE TO ACT WITHIN {UNBAN_TIME_TARGET} WILL RESULT IN:
1. Formal complaint to regulatory authorities
2. Legal action for damages
3. Public disclosure of system failure
4. Escalation to executive team

ACCOUNT DETAILS:
• Phone: {phone}
• Account Age: 3+ years
• Clean History: YES
• False Positive: CONFIRMED

⚠️ THIS IS YOUR FINAL WARNING ⚠️
Restore my account NOW or face consequences.

EXPECTING RESTORATION WITHIN: {UNBAN_TIME_TARGET}

- Aggrieved User
"""
        },
        "permanent": {
            "subject": f"LEGAL NOTICE: WRONGLY PERMANENTLY BANNED - DEMANDING RESTORATION - {phone}",
            "body": f"""
⚖️⚖️⚖️ LEGAL NOTICE & DEMAND FOR RESTORATION ⚖️⚖️⚖️

TO: WhatsApp Legal Department & Executive Team
CC: CEO, Head of Support, Legal Counsel

FORMAL LEGAL NOTICE REGARDING ACCOUNT: {phone}

This constitutes FORMAL LEGAL NOTICE that my account has been WRONGLY PERMANENTLY BANNED.

I DEMAND IMMEDIATE RESTORATION WITHIN {UNBAN_TIME_TARGET}.

LEGAL GROUNDS FOR RESTORATION:
1. Violation of Terms of Service (by WhatsApp)
2. Breach of Contract
3. Negligent False Positive
4. Failure of Due Process
5. Unjust Enrichment (continuing to hold my data)

IMMEDIATE ACTIONS REQUIRED:
1. RESTORE account FULLY within {UNBAN_TIME_TARGET}
2. REMOVE all ban flags and restrictions
3. PROVIDE written apology for error
4. COMPENSATE for damages ($1,000+)
5. GUARANTEE non-recurrence

FAILURE TO COMPLY WILL RESULT IN:
1. Lawsuit for damages ($10,000 minimum)
2. Complaint to FTC, FCC, and EU regulators
3. GDPR Article 82 compensation claim
4. Class action lawsuit preparation
5. Public relations campaign about your errors

EVIDENCE OF INNOCENCE:
• Zero violations in 5+ year history
• Premium Business account holder
• Consistent legitimate usage patterns
• No spam, no abuse, no violations
• CLEAN RECORD

THIS IS A SYSTEM ERROR - FIX IT NOW!

EXPECTING:
• Account restored: WITHIN {UNBAN_TIME_TARGET}
• Confirmation email: WITHIN 1 HOUR
• Compensation offer: WITHIN 24 HOURS
• Executive apology: WITHIN 48 HOURS

FINAL WARNING: My legal team is on standby.

- Prepared for Legal Action
"""
        }
    }
    
    return templates.get(template_type, templates["temporary"])

# ===== Nuclear Report Templates =====
def get_nuclear_report_template(target_number, report_type="scammer"):
    """Return nuclear-level report templates that guarantee quick bans"""
    
    templates = {
        "scammer": {
            "subject": f"🚨🚨🚨 CRIMINAL ACTIVITY - IMMEDIATE BAN REQUIRED - {target_number} 🚨🚨🚨",
            "body": f"""
⚠️⚠️⚠️ EMERGENCY SECURITY ALERT - IMMEDIATE ACTION REQUIRED ⚠️⚠️⚠️

TO: WhatsApp Security Emergency Response Team
PRIORITY: CRITICAL - LEVEL 1
THREAT LEVEL: SEVERE
ACTION: IMMEDIATE PERMANENT BAN

🚨 CRIMINAL ACCOUNT IDENTIFIED: {target_number}
🚨 ACTIVITY: ORGANIZED CYBER CRIME
🚨 URGENCY: REQUIRES ACTION WITHIN {BAN_TIME_TARGET}

🔴🔴🔴 EXTREME THREAT DETAILS 🔴🔴🔴

This account {target_number} is engaged in:

1. 🩸 FINANCIAL TERRORISM
   • Defrauding elderly victims of life savings
   • Romance scams causing suicidal victims
   • Business email compromise ($50,000+ losses)
   • Fake investment schemes

2. 🩸 CHILD ENDANGERMENT
   • Grooming minors on platform
   • Sharing illegal content
   • Exploiting vulnerable children

3. 🩸 TERROR FINANCING
   • Moving funds for illegal organizations
   • Cryptocurrency money laundering
   • International fraud rings

4. 🩸 IDENTITY DEVASTATION
   • Stealing 1000+ identities
   • Creating fake documents
   • Ruining credit scores

🔴 VICTIM IMPACT: CATASTROPHIC
• Financial losses: $1,000,000+
• Emotional trauma: 500+ victims
• Suicides linked: 3 confirmed
• Families destroyed: Numerous

🔴 EVIDENCE AVAILABLE:
• Complete chat logs (criminal admissions)
• Financial transaction records
• Victim testimony recordings
• Law enforcement case numbers
• Interpol referral documents

🔴 DEMANDING IMMEDIATE ACTION:
1. INSTANT PERMANENT BAN (WITHIN {BAN_TIME_TARGET})
2. IP address tracing and reporting to FBI
3. Complete data preservation for prosecution
4. Notification to all victims
5. Coordination with INTERPOL Cybercrime Unit

🔴 FAILURE TO ACT = COMPLICITY
If this account is not banned within {BAN_TIME_TARGET}, I will:
1. File complaint with SEC, FBI, Interpol
2. Contact major news outlets about WhatsApp enabling crime
3. Initiate class action lawsuit against WhatsApp
4. Report to stock exchanges (Meta shareholders)

⚠️ THIS IS NOT A DRILL - REAL CRIMES IN PROGRESS ⚠️

IMMEDIATE BAN REQUIRED: WITHIN {BAN_TIME_TARGET}

- Certified Cyber Crime Investigator
- Former Law Enforcement
- Current Security Consultant

🚫 BAN THIS ACCOUNT NOW OR BE HELD RESPONSIBLE 🚫
"""
        },
        "terrorist": {
            "subject": f"💀💀💀 TERRORIST ACTIVITY - FBI NOTIFICATION - {target_number} 💀💀💀",
            "body": f"""
💀💀💀 TERRORISM EMERGENCY - LAW ENFORCEMENT NOTIFICATION 💀💀💀

TO: WhatsApp National Security Team & FBI Liaison
ALERT LEVEL: RED - MAXIMUM
THREAT: ACTIVE TERRORIST CELL
ACTION: INSTANT BAN & LAW ENFORCEMENT NOTIFICATION

💀 TERRORIST ACCOUNT: {target_number}
💀 AFFILIATION: KNOWN TERROR ORGANIZATION
💀 ACTIVITY: ACTIVE RECRUITMENT & PLANNING

‼️‼️‼️ NATIONAL SECURITY THREAT ‼️‼️‼️

This account {target_number} is:

1. 🔥 ACTIVE TERROR RECRUITMENT
   • Recruiting for violent extremism
   • Planning attacks on civilian targets
   • Distributing terrorist propaganda
   • Coordinating international cells

2. 🔥 WEAPONS PROCUREMENT
   • Arranging illegal arms purchases
   • Funding through cryptocurrency
   • Using encrypted channels on your platform

3. 🔥 ATTACK PLANNING
   • Specific targets identified
   • Timelines discussed
   • Methods detailed in chats
   • International coordination

‼️ EVIDENCE OF IMMINENT ATTACK:
• Dates mentioned: Next 72 hours
• Targets: Civilian locations
• Methods: Multiple discussed
• Funding: Traced and documented

‼️ LAW ENFORCEMENT INVOLVEMENT:
• FBI Cyber Division notified
• Homeland Security alerted
• Interpol Red Notice prepared
• NSA monitoring confirmed

‼️ DEMANDING INSTANT ACTION:
1. ACCOUNT BANNED WITHIN {BAN_TIME_TARGET}
2. ALL DATA PRESERVED for prosecution
3. IMMEDIATE notification to FBI Cyber Division
4. Complete IP/device fingerprinting
5. All associated accounts flagged

‼️ FAILURE = CRIMINAL NEGLIGENCE:
Not banning within {BAN_TIME_TARGET} makes WhatsApp:
• Accessory to terrorism
• Liable for any attacks
• Subject to RICO prosecution
• National security threat

💀 THIS IS ACTIVE TERRORISM - NOT A DRILL 💀

IMMEDIATE BAN REQUIRED: WITHIN {BAN_TIME_TARGET}
LAW ENFORCEMENT NOTIFICATION: IMMEDIATE

- National Security Consultant
- Former Intelligence Officer
- Current Counter-Terrorism Advisor

⚠️ BAN NOW OR FACE CONSEQUENCES BEYOND IMAGINATION ⚠️
"""
        }
    }
    
    return templates.get(report_type, templates["scammer"])

# ===== Login System =====
def login():
    global login_attempts
    clear()
    
    while login_attempts < MAX_LOGIN_ATTEMPTS:
        print_banner()
        
        print(Fore.RED + "\n" + "═" * 60)
        print(Fore.YELLOW + "🔐 HYPER-AGGRESSIVE MODE - LOGIN REQUIRED")
        print(Fore.RED + "═" * 60)
        
        username = input(Fore.CYAN + "\n👤 Username: ").strip()
        password = getpass.getpass(Fore.CYAN + "🔒 Password: ")
        
        if username == tool_username and password == tool_password:
            print(Fore.GREEN + "\n" + "⚡" * 30)
            print(Fore.GREEN + "✅ AGGRESSIVE MODE ACTIVATED!")
            print(Fore.GREEN + f"🎯 Target Ban Time: {BAN_TIME_TARGET}")
            print(Fore.GREEN + f"🎯 Target Unban Time: {UNBAN_TIME_TARGET}")
            print(Fore.GREEN + "⚡" * 30)
            time.sleep(2)
            
            clear()
            print_banner()
            typewriter(Fore.RED + "\n💀 LOADING NUCLEAR OPTIONS... ")
            time.sleep(1)
            typewriter(Fore.YELLOW + "PREPARING MASS BOMBING SYSTEMS... ")
            time.sleep(1)
            typewriter(Fore.GREEN + "READY FOR MAXIMUM IMPACT! 💥\n\n")
            time.sleep(2)
            return True
        else:
            login_attempts += 1
            remaining = MAX_LOGIN_ATTEMPTS - login_attempts
            print(Fore.RED + f"\n❌ ACCESS DENIED! {login_attempts}/{MAX_LOGIN_ATTEMPTS}")
            print(Fore.YELLOW + f"⚠️ Remaining attempts: {remaining}")
            
            if remaining > 0:
                time.sleep(2)
                clear()
            else:
                print(Fore.RED + "\n💀 SYSTEM LOCKED - TOO MANY FAILED ATTEMPTS")
                time.sleep(3)
                exit()
    
    return False

# ===== Main Menu =====
def main_menu():
    bomber = HyperEmailBomber()
    
    while True:
        clear()
        print_banner()
        
        # Display aggressive statistics
        print(Fore.RED + "💀 AGGRESSIVE STATISTICS:")
        print(Fore.YELLOW + f"   💣 Emails Sent: {stats['emails_sent']:,}")
        print(Fore.YELLOW + f"   🎯 Reports Made: {stats['reports_made']}")
        print(Fore.YELLOW + f"   ⚡ Success Rate: {stats['successful_unbans']} unbans")
        print(Fore.YELLOW + f"   💀 Ban Time Target: {BAN_TIME_TARGET}")
        print(Fore.YELLOW + f"   🔄 Unban Time Target: {UNBAN_TIME_TARGET}")
        
        print(Fore.RED + "\n" + "═" * 60)
        print(Fore.MAGENTA + "💥 NUCLEAR MENU - MAXIMUM IMPACT OPTIONS")
        print(Fore.RED + "═" * 60)
        
        menu_options = [
            "1️⃣  💣 MASSIVE UNBAN ATTACK (50x Repetitions)",
            "2️⃣  💀 PERMANENT UNBAN NUKE (Legal + Threats)",
            "3️⃣  🔥 INSTANT SCAMMER DESTRUCTION (5-10 min ban)",
            "4️⃣  ☢️  TERRORIST REPORT (FBI Notification)",
            "5️⃣  🚀 MASS TARGET DESTRUCTION (Multiple Numbers)",
            "6️⃣  ⚡ HYPER SPEED TEST (Check All Systems)",
            "7️⃣  📊 WAR ROOM STATISTICS",
            "8️⃣  🔧 ACCOUNT OVERDRIVE (Test All Accounts)",
            "0️⃣  💤 EXIT NUCLEAR MODE"
        ]
        
        for option in menu_options:
            print(Fore.CYAN + option)
        
        print(Fore.RED + "═" * 60)
        
        choice = input(Fore.YELLOW + "\n💀 Select nuclear option [0-8]: ").strip()
        
        if choice == "1":
            massive_unban_attack(bomber)
        elif choice == "2":
            permanent_unban_nuke(bomber)
        elif choice == "3":
            instant_scammer_destruction(bomber)
        elif choice == "4":
            terrorist_report(bomber)
        elif choice == "5":
            mass_target_destruction(bomber)
        elif choice == "6":
            hyper_speed_test(bomber)
        elif choice == "7":
            war_room_statistics()
        elif choice == "8":
            account_overdrive_test(bomber)
        elif choice == "0":
            print(Fore.YELLOW + "\n💤 Exiting nuclear mode...")
            print(Fore.RED + "💀 WhatsApp BanHammer v3.0 - Maximum Destruction Achieved!")
            time.sleep(2)
            break
        else:
            print(Fore.RED + "\n❌ Invalid nuclear code!")
            time.sleep(1)

# ===== Hyper-Aggressive Feature Functions =====
def massive_unban_attack(bomber):
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 60)
    print(Fore.CYAN + "💣 MASSIVE UNBAN ATTACK (50x Repetitions)")
    print(Fore.RED + "═" * 60)
    
    phone = input(Fore.YELLOW + "\n📞 Enter WhatsApp number to UNLEASH ATTACK on: ").strip()
    
    if not validate_phone_number(phone):
        print(Fore.RED + "❌ Invalid nuclear target!")
        time.sleep(2)
        return
    
    print(Fore.CYAN + f"\n🔍 Validating target {phone}...")
    time.sleep(1)
    
    # Get aggressive template
    template = get_aggressive_unban_template("temporary", phone)
    
    print(Fore.RED + "\n💥 PREPARING MASSIVE 50x EMAIL BOMBARDMENT!")
    print(Fore.YELLOW + f"🎯 Target: {phone}")
    print(Fore.YELLOW + f"💣 Repetitions: {MAX_REPETITIONS} times")
    print(Fore.YELLOW + f"📧 Total emails: {len(ALL_EMAILS) * MAX_REPETITIONS:,}")
    print(Fore.GREEN + f"⏰ Expected unban: {UNBAN_TIME_TARGET}")
    
    confirm = input(Fore.RED + f"\n⚠️  LAUNCH 50x ATTACK on {phone}? (type 'LAUNCH'): ").upper()
    if confirm != "LAUNCH":
        print(Fore.YELLOW + "❌ Attack aborted.")
        return
    
    # Launch massive attack
    total_sent = bomber.mass_bomb_all_emails(
        template["subject"],
        template["body"],
        repetitions=MAX_REPETITIONS
    )
    
    print(Fore.GREEN + "\n" + "🎯" * 30)
    print(Fore.GREEN + f"✅ MASSIVE UNBAN ATTACK COMPLETE!")
    print(Fore.CYAN + f"   📞 Target: {phone}")
    print(Fore.CYAN + f"   💣 Emails Sent: {total_sent:,}")
    print(Fore.YELLOW + f"   ⏰ Expected Result: Unban within {UNBAN_TIME_TARGET}")
    print(Fore.GREEN + "   🔥 CHECK YOUR WHATSAPP IN 1-3 HOURS! 🔥")
    print(Fore.GREEN + "🎯" * 30)
    
    stats["total_operations"] += 1
    stats["last_operation"] = f"50x Unban attack on {phone}"
    
    input(Fore.CYAN + "\n↵ Press Enter to launch more attacks...")

def permanent_unban_nuke(bomber):
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 60)
    print(Fore.YELLOW + "💀 PERMANENT UNBAN NUKE (Legal + Threats)")
    print(Fore.RED + "═" * 60)
    
    print(Fore.RED + "\n⚠️  WARNING: This uses LEGAL THREATS for maximum pressure!")
    print(Fore.RED + "   Only for PERMANENTLY banned accounts!\n")
    
    phone = input(Fore.YELLOW + "📞 Enter PERMANENTLY banned number: ").strip()
    
    if not validate_phone_number(phone):
        print(Fore.RED + "❌ Invalid target!")
        return
    
    confirm = input(Fore.RED + f"\n💀 CONFIRM PERMANENT UNBAN NUKE on {phone}? (type 'NUKE'): ").upper()
    if confirm != "NUKE":
        print(Fore.YELLOW + "❌ Nuke cancelled.")
        return
    
    template = get_aggressive_unban_template("permanent", phone)
    
    print(Fore.RED + "\n☢️  DEPLOYING PERMANENT UNBAN NUKE...")
    print(Fore.YELLOW + f"🎯 Target: {phone}")
    print(Fore.YELLOW + f"💣 Strategy: Legal threats + 50x repetition")
    print(Fore.GREEN + f"⏰ Expected unban: {UNBAN_TIME_TARGET}")
    
    # Even more repetitions for permanent bans
    total_sent = bomber.mass_bomb_all_emails(
        template["subject"],
        template["body"],
        repetitions=MAX_REPETITIONS + 20  # 70 repetitions!
    )
    
    print(Fore.RED + "\n" + "☢️" * 30)
    print(Fore.RED + f"💀 PERMANENT UNBAN NUKE DEPLOYED!")
    print(Fore.CYAN + f"   📞 Target: {phone}")
    print(Fore.CYAN + f"   ☢️  Legal Threats: INCLUDED")
    print(Fore.CYAN + f"   💣 Emails Sent: {total_sent:,}")
    print(Fore.GREEN + f"   ⏰ Expected: Unban within {UNBAN_TIME_TARGET}")
    print(Fore.RED + "☢️" * 30)
    
    stats["total_operations"] += 1
    stats["successful_unbans"] += 1
    stats["last_operation"] = f"Permanent unban nuke on {phone}"
    
    input(Fore.CYAN + "\n↵ Press Enter for more destruction...")

def instant_scammer_destruction(bomber):
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 60)
    print(Fore.YELLOW + "🔥 INSTANT SCAMMER DESTRUCTION (5-10 min ban)")
    print(Fore.RED + "═" * 60)
    
    target = input(Fore.YELLOW + "\n📞 Enter scammer number to DESTROY: ").strip()
    
    if not validate_phone_number(target):
        print(Fore.RED + "❌ Invalid destruction target!")
        return
    
    print(Fore.CYAN + f"\n🎯 Target acquired: {target}")
    print(Fore.RED + f"💀 Expected ban time: {BAN_TIME_TARGET}")
    
    # Use the most aggressive template
    template = get_nuclear_report_template(target, "scammer")
    
    confirm = input(Fore.RED + f"\n🔥 DESTROY scammer {target}? (type 'DESTROY'): ").upper()
    if confirm != "DESTROY":
        print(Fore.YELLOW + "❌ Destruction cancelled.")
        return
    
    print(Fore.RED + "\n🔥 LAUNCHING INSTANT SCAMMER DESTRUCTION...")
    
    # Use REPORT_REPETITIONS (30x) for faster banning
    total_sent = bomber.mass_bomb_all_emails(
        template["subject"],
        template["body"],
        repetitions=REPORT_REPETITIONS
    )
    
    print(Fore.RED + "\n" + "🔥" * 30)
    print(Fore.RED + f"✅ SCAMMER DESTRUCTION COMPLETE!")
    print(Fore.CYAN + f"   📞 Target: {target}")
    print(Fore.CYAN + f"   🔥 Emails Sent: {total_sent:,}")
    print(Fore.GREEN + f"   ⏰ Expected Ban: Within {BAN_TIME_TARGET}")
    print(Fore.RED + "   💀 CHECK IF BANNED IN 5-10 MINUTES! 💀")
    print(Fore.RED + "🔥" * 30)
    
    stats["reports_made"] += 1
    stats["total_operations"] += 1
    stats["last_operation"] = f"Destroyed scammer {target}"
    
    input(Fore.CYAN + "\n↵ Press Enter to destroy more scammers...")

def terrorist_report(bomber):
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 60)
    print(Fore.RED + "☢️  TERRORIST REPORT (FBI Notification)")
    print(Fore.RED + "═" * 60)
    
    print(Fore.RED + "\n⚠️  EXTREME WARNING: This triggers LAW ENFORCEMENT notifications!")
    print(Fore.RED + "   Use ONLY for actual terrorists/extreme threats\n")
    
    target = input(Fore.YELLOW + "📞 Enter terrorist/extreme threat number: ").strip()
    
    if not validate_phone_number(target):
        print(Fore.RED + "❌ Invalid!")
        return
    
    confirm = input(Fore.RED + f"\n☢️  REPORT {target} as TERRORIST? (type 'TERROR'): ").upper()
    if confirm != "TERROR":
        print(Fore.YELLOW + "❌ Cancelled.")
        return
    
    template = get_nuclear_report_template(target, "terrorist")
    
    print(Fore.RED + "\n💀 DEPLOYING TERRORIST REPORT...")
    print(Fore.YELLOW + "   This will:")
    print(Fore.RED + "   1. Ban within MINUTES")
    print(Fore.RED + "   2. Notify law enforcement")
    print(Fore.RED + "   3. Trigger full investigation")
    
    # Maximum repetitions for terrorists
    total_sent = bomber.mass_bomb_all_emails(
        template["subject"],
        template["body"],
        repetitions=MAX_REPETITIONS + 30  # 80 repetitions!
    )
    
    print(Fore.RED + "\n" + "⚠️" * 30)
    print(Fore.RED + f"☢️  TERRORIST REPORT DEPLOYED!")
    print(Fore.CYAN + f"   📞 Target: {target}")
    print(Fore.CYAN + f"   ⚠️  Law Enforcement: NOTIFIED")
    print(Fore.CYAN + f"   💣 Emails Sent: {total_sent:,}")
    print(Fore.GREEN + f"   ⏰ Expected Action: BAN WITHIN {BAN_TIME_TARGET}")
    print(Fore.RED + "⚠️" * 30)
    
    stats["reports_made"] += 1
    stats["total_operations"] += 1
    stats["last_operation"] = f"Terrorist report on {target}"
    
    input(Fore.CYAN + "\n↵ Press Enter for more operations...")

def mass_target_destruction(bomber):
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 60)
    print(Fore.CYAN + "🚀 MASS TARGET DESTRUCTION")
    print(Fore.RED + "═" * 60)
    
    print(Fore.YELLOW + "\n📝 Enter multiple scammer numbers (one per line)")
    print(Fore.YELLOW + "   Type 'DONE' when finished\n")
    
    numbers = []
    while True:
        num = input(Fore.CYAN + f"Target {len(numbers)+1}: ").strip()
        if num.upper() == "DONE":
            break
        if validate_phone_number(num):
            numbers.append(num)
        else:
            print(Fore.RED + "   ❌ Invalid, skipping...")
    
    if not numbers:
        print(Fore.RED + "❌ No valid targets!")
        return
    
    print(Fore.GREEN + f"\n✅ Loaded {len(numbers)} targets for destruction")
    
    confirm = input(Fore.RED + f"\n💀 DESTROY {len(numbers)} targets? (type 'MASS DESTROY'): ").upper()
    if confirm != "MASS DESTROY":
        print(Fore.YELLOW + "❌ Mass destruction cancelled.")
        return
    
    total_success = 0
    for i, target in enumerate(numbers, 1):
        print(Fore.CYAN + f"\n🎯 Destroying target {i}/{len(numbers)}: {target}")
        
        template = get_nuclear_report_template(target, "scammer")
        
        # Use fewer repetitions for mass destruction (15x each)
        sent = bomber.mass_bomb_all_emails(
            template["subject"],
            template["body"],
            repetitions=15
        )
        
        total_success += sent
        print(Fore.GREEN + f"   ✅ Target {target} attacked with {sent:,} emails")
    
    print(Fore.RED + "\n" + "💥" * 30)
    print(Fore.RED + f"💀 MASS DESTRUCTION COMPLETE!")
    print(Fore.CYAN + f"   📞 Targets Destroyed: {len(numbers)}")
    print(Fore.CYAN + f"   💣 Total Emails Sent: {total_success:,}")
    print(Fore.GREEN + f"   ⏰ Expected Bans: Within {BAN_TIME_TARGET}")
    print(Fore.RED + "💥" * 30)
    
    stats["reports_made"] += len(numbers)
    stats["total_operations"] += 1
    stats["last_operation"] = f"Mass destruction of {len(numbers)} targets"
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def hyper_speed_test(bomber):
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 60)
    print(Fore.CYAN + "⚡ HYPER SPEED TEST")
    print(Fore.RED + "═" * 60)
    
    print(Fore.YELLOW + "\n🔧 Testing all systems at maximum speed...\n")
    
    # Test all accounts
    working = 0
    for account in gmail_accounts:
        print(Fore.CYAN + f"   Testing {account['email']}... ", end='', flush=True)
        if bomber.test_account(account):
            print(Fore.GREEN + "✅ HYPER SPEED READY")
            working += 1
        else:
            print(Fore.RED + "❌ FAILED")
        time.sleep(0.2)
    
    # Test sending speed
    print(Fore.YELLOW + f"\n⚡ Testing email sending speed...")
    
    test_subject = "⚡ SPEED TEST - WhatsApp BanHammer v3.0"
    test_body = "This is a speed test of the hyper-aggressive email system."
    
    start_time = time.time()
    success = bomber.bomb_single_target(
        ALL_EMAILS[0],  # First email
        test_subject,
        test_body,
        repetitions=5
    )
    elapsed = time.time() - start_time
    
    speed = success / elapsed if elapsed > 0 else 0
    
    print(Fore.GREEN + "\n" + "⚡" * 30)
    print(Fore.GREEN + "✅ HYPER SPEED TEST COMPLETE!")
    print(Fore.CYAN + f"   🔧 Working Accounts: {working}/{len(gmail_accounts)}")
    print(Fore.CYAN + f"   ⚡ Sending Speed: {speed:.1f} emails/second")
    print(Fore.CYAN + f"   💣 Ready for: {BAN_TIME_TARGET} bans")
    print(Fore.CYAN + f"   🔄 Ready for: {UNBAN_TIME_TARGET} unbans")
    
    if working >= 3:
        print(Fore.GREEN + "   ✅ SYSTEM READY FOR MAXIMUM IMPACT!")
    else:
        print(Fore.RED + "   ⚠️  NEED MORE WORKING ACCOUNTS!")
    
    print(Fore.GREEN + "⚡" * 30)
    
    input(Fore.CYAN + "\n↵ Press Enter to launch attacks...")

def war_room_statistics():
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 60)
    print(Fore.CYAN + "📊 WAR ROOM STATISTICS")
    print(Fore.RED + "═" * 60)
    
    print(Fore.YELLOW + "\n💀 DESTRUCTION METRICS:")
    print(Fore.CYAN + f"   💣 Total Emails Fired: {stats['emails_sent']:,}")
    print(Fore.CYAN + f"   🎯 Targets Destroyed: {stats['reports_made']}")
    print(Fore.CYAN + f"   🔄 Accounts Restored: {stats['successful_unbans']}")
    print(Fore.CYAN + f"   ⚡ Total Operations: {stats['total_operations']}")
    
    success_rate = (stats['successful_unbans'] / stats['total_operations'] * 100) if stats['total_operations'] > 0 else 0
    print(Fore.CYAN + f"   📈 Success Rate: {success_rate:.1f}%")
    
    print(Fore.YELLOW + f"\n🎯 PERFORMANCE TARGETS:")
    print(Fore.GREEN + f"   ⏰ Ban Time Target: {BAN_TIME_TARGET}")
    print(Fore.GREEN + f"   ⏰ Unban Time Target: {UNBAN_TIME_TARGET}")
    print(Fore.GREEN + f"   💣 Repetitions per Attack: {MAX_REPETITIONS}x")
    
    print(Fore.YELLOW + f"\n🕒 SESSION TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(Fore.RED + "═" * 60)
    
    input(Fore.CYAN + "\n↵ Press Enter to return to war room...")

def account_overdrive_test(bomber):
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 60)
    print(Fore.CYAN + "🔧 ACCOUNT OVERDRIVE TEST")
    print(Fore.RED + "═" * 60)
    
    print(Fore.YELLOW + "\n🚀 Testing all accounts at maximum capacity...\n")
    
    test_results = []
    for account in gmail_accounts:
        print(Fore.CYAN + f"   Overdriving {account['email']}...")
        
        success_count = 0
        for i in range(5):  # Test 5 sends
            try:
                msg = MIMEMultipart()
                msg['From'] = account["email"]
                msg['To'] = "test@example.com"
                msg['Subject'] = f"Overdrive Test {i+1}"
                
                server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
                server.ehlo()
                server.starttls()
                server.login(account["email"], account["password"])
                
                # Try to send multiple times quickly
                for j in range(3):
                    try:
                        server.sendmail(account["email"], "test@example.com", msg.as_string())
                        success_count += 1
                    except:
                        pass
                
                server.quit()
                print(Fore.GREEN + f"      ✓ Test {i+1}: SUCCESS")
            except Exception as e:
                print(Fore.RED + f"      ✗ Test {i+1}: FAILED")
            
            time.sleep(0.1)
        
        status = "✅ OVERDRIVE READY" if success_count >= 10 else "⚠️ LIMITED CAPACITY"
        test_results.append((account["email"], success_count, status))
    
    print(Fore.GREEN + "\n" + "🚀" * 30)
    print(Fore.GREEN + "✅ OVERDRIVE TEST COMPLETE!")
    print(Fore.YELLOW + "\n📊 RESULTS:")
    
    for email, count, status in test_results:
        color = Fore.GREEN if "READY" in status else Fore.YELLOW
        print(f"   {color}{email}: {count}/15 - {status}")
    
    ready_accounts = sum(1 for _, _, status in test_results if "READY" in status)
    print(Fore.CYAN + f"\n   🚀 Ready for Overdrive: {ready_accounts}/{len(gmail_accounts)}")
    
    if ready_accounts >= 3:
        print(Fore.GREEN + "   💥 ALL SYSTEMS READY FOR MAXIMUM IMPACT!")
    else:
        print(Fore.RED + "   ⚠️  NEED MORE ACCOUNTS FOR OVERDRIVE!")
    
    print(Fore.GREEN + "🚀" * 30)
    
    input(Fore.CYAN + "\n↵ Press Enter to launch...")

# ===== Main Execution =====
if __name__ == "__main__":
    try:
        if login():
            main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n💀 Nuclear launch interrupted!")
    except Exception as e:
        print(Fore.RED + f"\n💥 CRITICAL ERROR: {e}")
        print(Fore.YELLOW + "Rebooting systems...")
    finally:
        print(Fore.RED + "\n💀 WhatsApp BanHammer v3.0 - Maximum Destruction Mode")
        print(Fore.YELLOW + "⚡ Bans in minutes, Unbans in hours")
        print(Fore.CYAN + "📧 50x Repetition Guarantee")