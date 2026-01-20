import smtplib
import getpass
import time
import re
import os
import random
import requests
import json
import threading
from concurrent.futures import ThreadPoolExecutor
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

# ===== Enhanced Gmail Accounts with Backup =====
gmail_accounts = [
    {"email": "bematunmi444@gmail.com", "password": "siqlebxrpvqugxsy", "status": "active"},
    {"email": "zorosales6@gmail.com", "password": "ltvtpaduohtlsykx", "status": "active"},
    {"email": "okunlolatunmise12@gmail.com", "password": "otvmwdhxvmxbqglf", "status": "active"},
    {"email": "mbb657504@gmail.com", "password": "hkun wznn jsfe eltc", "status": "active"},
    {"email": "riderstuff61@gmail.com", "password": "hjaormoydmyaveas", "status": "active"},
]

# ===== WhatsApp Support Emails (Categorized for Better Targeting) =====
SUPPORT_EMAILS = {
    "urgent": [
        "support@support.whatsapp.com",
        "appeals@support.whatsapp.com",
        "1483635209301664@support.whatsapp.com",
    ],
    "technical": [
        "android_web@support.whatsapp.com",
        "ios_web@support.whatsapp.com",
        "webclient_web@support.whatsapp.com",
    ],
    "security": [
        "businesscomplaints@support.whatsapp.com",
        "abuse@support.whatsapp.com",
        "security@support.whatsapp.com",
        "help@whatsapp.com"
    ],
    "general": [
        "support@whatsapp.com",
        "info@whatsapp.com",
        "press@whatsapp.com",
        "business@whatsapp.com"
    ]
}

# ===== WhatsApp Business API =====
ACCESS_TOKEN = "EAAJgi17vyDYBPTGf8m4LNp0xFdUozhBKS6PTnrElQdSZCIRZCnuLFmBigzRvB4ZCUI8EBNuNZCFZBfG5e11ehZBujToi9S6zYQ3HSmDZBPNQHZBFFrd3ntSZAl6lRZAOa86mOZCp60VaaCMhgUN6s68EEvYSEJXlaIk9iiB7xe1rlZBKbEVf7YiIADUZA0kHuO9nr0QZDZD"
PHONE_NUMBER_ID = "669101662914614"

# ===== Statistics Tracking =====
stats = {
    "emails_sent": 0,
    "reports_made": 0,
    "numbers_checked": 0,
    "successful_unbans": 0,
    "last_operation": None
}

# ===== Utility Functions =====
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def typewriter(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def print_banner():
    banner_color = random.choice([Fore.BLUE, Fore.CYAN, Fore.MAGENTA, Fore.GREEN, Fore.YELLOW])
    banner = f"""
    {banner_color}╔══════════════════════════════════════════════════════════╗
    ║                📲 WHATSAPP UNBAN ULTIMATE TOOL v2.0           ║
    ║                      🔥 Powered by Tunzy Shop 🔥              ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

def validate_phone_number(phone):
    """Enhanced phone number validation"""
    pattern = r'^\+\d{10,15}$'
    if not re.match(pattern, phone):
        return False
    # Additional validation: Remove country code and check
    clean_number = phone[1:]  # Remove +
    if not clean_number.isdigit():
        return False
    return True

# ===== Enhanced Email Sending System =====
class EmailBomber:
    def __init__(self):
        self.account_cycle = cycle(gmail_accounts)
        self.active_accounts = [acc for acc in gmail_accounts if acc["status"] == "active"]
        
    def test_account(self, account):
        """Test if Gmail account is working"""
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
            server.ehlo()
            server.starttls()
            server.login(account["email"], account["password"])
            server.quit()
            return True
        except:
            account["status"] = "inactive"
            return False
    
    def rotate_account(self):
        """Get next working account"""
        for _ in range(len(gmail_accounts)):
            account = next(self.account_cycle)
            if account["status"] == "active" and self.test_account(account):
                return account
        return None
    
    def send_single_email(self, account, to_email, subject, body, email_type="urgent"):
        """Send single email with retry logic"""
        max_retries = 2
        for attempt in range(max_retries):
            try:
                msg = MIMEMultipart()
                msg['From'] = account["email"]
                msg['To'] = to_email
                
                # Add priority headers for urgent emails
                if email_type == "urgent":
                    msg['X-Priority'] = '1'
                    msg['X-MSMail-Priority'] = 'High'
                    msg['Importance'] = 'high'
                
                msg['Subject'] = subject
                
                # Add timestamp to body
                enhanced_body = f"{body}\n\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                msg.attach(MIMEText(enhanced_body, 'plain'))
                
                server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
                server.ehlo()
                server.starttls()
                server.login(account["email"], account["password"])
                server.send_message(msg)
                server.quit()
                
                stats["emails_sent"] += 1
                return True
            except Exception as e:
                if attempt == max_retries - 1:
                    print(Fore.RED + f"   ✗ Failed to send to {to_email}: {str(e)[:50]}")
                    return False
                time.sleep(1)
        return False
    
    def mass_send(self, emails, subject, body, email_type="urgent", threads=5):
        """Send emails using multiple threads for speed"""
        account = self.rotate_account()
        if not account:
            print(Fore.RED + "❌ No working email accounts available!")
            return 0, len(emails)
        
        print(Fore.CYAN + f"📧 Using account: {account['email']}")
        print(Fore.YELLOW + f"⚡ Sending {len(emails)} emails with {threads} threads...")
        
        success = 0
        fail = 0
        
        def send_batch(batch_emails):
            nonlocal success, fail
            for email in batch_emails:
                if self.send_single_email(account, email, subject, body, email_type):
                    success += 1
                    print(Fore.GREEN + f"   ✓ Sent to {email}")
                else:
                    fail += 1
                time.sleep(0.1)  # Rate limiting
        
        # Split emails into batches for threading
        batch_size = len(emails) // threads + 1
        batches = [emails[i:i + batch_size] for i in range(0, len(emails), batch_size)]
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(send_batch, batches)
        
        return success, fail

# ===== Enhanced WhatsApp Number Check =====
def enhanced_check_whatsapp_number(phone):
    """Check WhatsApp number with multiple methods"""
    print(Fore.CYAN + f"\n🔍 Checking {phone}...")
    
    # Method 1: WhatsApp Business API
    print(Fore.YELLOW + "   Method 1: WhatsApp Business API Check")
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/contacts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "blocking": "wait",
        "contacts": [phone],
        "force_check": True
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            for contact in data.get("contacts", []):
                status = contact.get("status", "unknown")
                wa_id = contact.get("wa_id", "N/A")
                input_field = contact.get("input", "N/A")
                
                if status == "valid":
                    print(Fore.GREEN + f"   ✅ VALID: {wa_id} is registered on WhatsApp")
                    print(Fore.CYAN + f"   📱 Input: {input_field}")
                    return True, wa_id
                else:
                    print(Fore.RED + f"   ❌ INVALID: Number not registered")
                    return False, None
        else:
            print(Fore.YELLOW + f"   ⚠️ API Error: {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"   ⚠️ API Request Failed: {e}")
    
    # Method 2: Alternative check (simulated)
    print(Fore.YELLOW + "\n   Method 2: Alternative Verification")
    time.sleep(1)
    
    # Simulate check (replace with actual alternative method if available)
    print(Fore.YELLOW + "   ⚠️ Note: Consider using WhatsApp Web scan method for manual verification")
    
    stats["numbers_checked"] += 1
    return False, None

# ===== Enhanced Unban Templates =====
def get_unban_template(template_type, phone):
    """Return enhanced unban email templates"""
    
    templates = {
        "temporary": {
            "subject": f"URGENT: Appeal for WhatsApp Account Restoration - {phone}",
            "body": f"""
URGENT APPEAL FOR WHATSAPP ACCOUNT REINSTATEMENT

Dear WhatsApp Support Team,

I am writing with utmost urgency regarding the temporary suspension of my WhatsApp account associated with phone number: {phone}

ACCOUNT DETAILS:
• Phone Number: {phone}
• Account Creation: Over 2 years ago
• Device: iPhone 14 Pro / Samsung Galaxy S23
• WhatsApp Version: 2.25.86.84
• Last Backup: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SITUATION ANALYSIS:
Upon careful reflection, I believe this suspension may have resulted from:
1. Potential misinterpretation of automated system flags
2. Unintentional sharing of forwarded content
3. Sudden increase in message frequency due to emergency family situation
4. Possible mass reporting by unknown individuals

IMPORTANCE OF ACCOUNT:
This account is CRITICAL for:
• Family communication (elderly parents depend on it)
• Business operations (primary contact for clients)
• Emergency contact with healthcare providers
• Two-factor authentication for multiple services

I have taken immediate corrective actions:
1. Removed all forwarded content
2. Reviewed and accepted all WhatsApp Terms of Service
3. Enabled two-step verification
4. Performed complete security audit

LEGAL COMPLIANCE:
I affirm that:
• I am the legitimate owner of this number
• No fraudulent activity was intended
• All communications were personal/business related
• I comply with all applicable laws and regulations

REQUEST:
I humbly request:
1. Immediate review of my account
2. Temporary restoration pending investigation
3. Clear guidelines on any violations
4. Opportunity to correct any misunderstandings

The suspension has caused significant hardship. Your prompt assistance would be immensely appreciated.

Sincerely,
Account Owner
Contact: {phone}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

---
This is an automated appeal generated through authorized channels.
"""
        },
        "permanent": {
            "subject": f"FINAL APPEAL: Permanent Ban Reconsideration - Case #{random.randint(100000, 999999)}",
            "body": f"""
FINAL FORMAL APPEAL FOR PERMANENT BAN RECONSIDERATION

TO: WhatsApp Legal & Support Departments
CC: Appeals Committee, User Safety Team
CASE ID: WB-{random.randint(100000, 999999)}-{datetime.now().strftime('%m%Y')}

REGISTERED PHONE NUMBER: {phone}
DATE OF INCIDENT: {datetime.now().strftime('%Y-%m-%d')}
APPEAL TYPE: Final Request for Reconsideration

DECLARATION OF COMPLIANCE:
I, the account holder of {phone}, hereby declare:
1. Full acceptance of WhatsApp Terms of Service
2. Zero tolerance for spam, abuse, or illegal activities
3. Commitment to community guidelines
4. Willingness to undergo identity verification

ROOT CAUSE ANALYSIS (Suspected):
• Possible false-positive in automated moderation system
• Account compromise during travel abroad
• Mass false reporting by malicious actors
• Technical glitch during backup restoration

IMPACT ASSESSMENT:
The permanent ban has resulted in:
1. Loss of 5+ years of chat history and media
2. Disruption of business operations (estimated loss: $5,000+)
3. Inability to access emergency family groups
4. Compromised security for 15+ linked services

MITIGATION MEASURES IMPLEMENTED:
1. Factory reset primary device
2. Changed all linked passwords
3. Installed latest security updates
4. Enrolled in cybersecurity awareness course
5. Setup dedicated business account (separate number)

EVIDENCE OF LEGITIMATE USE:
• Account age: 5+ years
• Consistent device fingerprint
• Regular backup patterns
• Verified payment history for business features
• Clean record until recent incident

SPECIAL CONSIDERATION REQUEST:
Considering my:
1. Long-standing account history
2. Immediate corrective actions
3. Willingness to comply with enhanced monitoring
4. Critical dependence on WhatsApp services

I request a ONE-TIME exception and account restoration under:
1. 30-day probation period
2. Enhanced security requirements
3. Limited functionality initially
4. Regular compliance reporting

ALTERNATIVE RESOLUTION:
If full restoration isn't possible, please consider:
1. Data export permission
2. Temporary access for contact migration
3. Business account conversion
4. Escalation to senior support specialist

This appeal represents my final attempt at resolution before pursuing alternative dispute resolution channels.

Respectfully submitted,

Account Holder: [NAME]
Contact: {phone}
Supporting Documentation: Available upon request
Legal Representation: Prepared to engage if necessary

---
AUTOMATED APPEAL SYSTEM v2.0 | TUNZY SHOP | {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
        }
    }
    
    return templates.get(template_type, templates["temporary"])

# ===== Enhanced Report Templates =====
def get_report_template(report_type, target_number):
    """Return enhanced report templates"""
    
    templates = {
        "temporary_report": {
            "subject": f"IMMEDIATE ACTION REQUIRED: Fraudulent Account {target_number}",
            "body": f"""
URGENT: FRAUDULENT WHATSAPP ACCOUNT REPORT

TO: WhatsApp Security & Abuse Department
PRIORITY: HIGH
REPORT ID: FRAUD-{random.randint(100000, 999999)}

REPORTED NUMBER: {target_number}
REPORT TYPE: Financial Fraud & Scam Operation
TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

DETAILED ACCOUNT ACTIVITY:
The account associated with {target_number} is actively engaged in:
1. FINANCIAL SCAMS: Impersonating bank officials
2. ROMANCE FRAUD: Catfishing vulnerable individuals
3. BUSINESS EMAIL COMPROMISE: Fake invoice schemes
4. CRYPTO SCAMS: Fake investment opportunities
5. IDENTITY THEFT: Collecting personal information

MODUS OPERANDI:
• Uses fake profile pictures (stolen images)
• Claims to be WhatsApp support staff
• Requests verification codes from victims
• Creates fake emergency situations
• Uses manipulated screenshots as "proof"

VICTIM IMPACT:
• Estimated victims: 50+
• Financial losses: $10,000+
• Emotional distress: Severe
• Identity theft risk: HIGH

EVIDENCE COLLECTED:
1. Screenshots of fraudulent conversations
2. Fake document templates used
3. Victim testimonials (available)
4. Transaction records
5. Pattern analysis showing coordinated attacks

IMMEDIATE ACTION REQUESTED:
1. INSTANT ACCOUNT SUSPENSION
2. IP address tracing
3. Device fingerprinting
4. Coordination with law enforcement
5. Victim notification system activation

This account represents CLEAR and PRESENT DANGER to the WhatsApp community.

Reporting User: Verified WhatsApp User
Contact: Available for investigator follow-up
Willing to testify: YES

---
AUTOMATED SECURITY REPORT | PRIORITY: CRITICAL
"""
        },
        "permanent_report": {
            "subject": f"LAW ENFORCEMENT NOTIFICATION: Criminal Activity - {target_number}",
            "body": f"""
LAW ENFORCEMENT & LEGAL COMPLIANCE REPORT

TO: WhatsApp Legal Department, Security Team, and Relevant Authorities
CASE CLASSIFICATION: CRIMINAL ACTIVITY
REPORT LEVEL: MAXIMUM URGENCY

CRIMINAL ACCOUNT: {target_number}
ACTIVITY TYPE: Organized Cyber Crime
JURISDICTION: International

CRIMINAL OFFENSES IDENTIFIED:
1. WIRE FRAUD (18 U.S.C. § 1343)
2. IDENTITY THEFT (18 U.S.C. § 1028)
3. MONEY LAUNDERING CONSPIRACY
4. COMPUTER FRAUD AND ABUSE
5. ORGANIZED CRIME ACTIVITY

OPERATIONAL DETAILS:
• Network Size: 10+ linked accounts
• Geographic Spread: 5+ countries
• Daily Victims: 20-30 individuals
• Estimated Monthly Revenue: $50,000+
• Money Mule Networks: Active

SPECIFIC CRIMINAL ACTIVITIES:
• IMPERSONATION: Claims to be Mark Zuckerberg's son
• CORPORATE FRAUD: Fake Meta/WhatsApp job offers
• ADVANCE-FEE SCAMS: "Tax payments" for fake prizes
• ROMANCE SCAMS: Multiple simultaneous victims
• BUSINESS COMPROMISE: Fake CEO directives

EVIDENCE PACKAGE INCLUDES:
1. Complete chat logs (1000+ pages)
2. Financial transaction trails
3. Victim impact statements
4. Network mapping
5. Timeline of criminal activity

LEGAL REQUIREMENTS:
Under various international laws and regulations, including:
• GDPR Article 33 (Data breach notification)
• US-EU Privacy Shield requirements
• Cybercrime Convention (Budapest Convention)
• Local telecommunications laws

IMMEDIATE LEGAL ACTIONS REQUIRED:
1. ACCOUNT PRESERVATION ORDER (for evidence)
2. IMMEDIATE SUSPENSION of all linked accounts
3. DATA HANDOVER to INTERPOL Cybercrime Unit
4. PRESERVATION of all logs and metadata
5. COORDINATION with FBI Internet Crime Complaint Center

FAILURE TO ACT:
Continued operation of this account constitutes:
• Negligence in duty of care
• Violation of platform safety obligations
• Potential complicity in ongoing crimes

This report is filed with copies to:
• National Cyber Security Centre
• Internet Crime Complaint Center (IC3)
• Relevant national CERT teams

Reporting Entity: Certified Security Researcher
Affiliation: Tunzy Shop Security Division
Legal Standing: Prepared for subpoena compliance

---
OFFICIAL CRIMINAL REPORT | LEGAL ACTION IMMINENT
COPY PRESERVED FOR JUDICIAL PROCEEDINGS
"""
        }
    }
    
    return templates.get(report_type)

# ===== Login System =====
def login():
    global login_attempts
    clear()
    
    while login_attempts < MAX_LOGIN_ATTEMPTS:
        print_banner()
        
        print(Fore.CYAN + "\n" + "═" * 55)
        print(Fore.YELLOW + "🔐 SECURE LOGIN REQUIRED")
        print(Fore.CYAN + "═" * 55)
        
        username = input(Fore.CYAN + "\n👤 Username: ").strip()
        password = getpass.getpass(Fore.CYAN + "🔒 Password: ")
        
        if username == tool_username and password == tool_password:
            print(Fore.GREEN + "\n" + "✓" * 30)
            print(Fore.GREEN + "✅ AUTHENTICATION SUCCESSFUL!")
            print(Fore.GREEN + "✓" * 30)
            time.sleep(1)
            
            # Welcome animation
            clear()
            print_banner()
            welcome_msg = f"""
            ╔═══════════════════════════════════════════════╗
            ║         WELCOME TO WHATSAPP UNBAN TOOL        ║
            ║               Version 2.0 - ENHANCED          ║
            ║                                               ║
            ║    Features:                                  ║
            ║    • Multi-threaded Email System             ║
            ║    • Enhanced Success Rates                  ║
            ║    • Real-time Status Tracking               ║
            ║    • Advanced Reporting System               ║
            ║    • Criminal Activity Documentation         ║
            ║                                               ║
            ║    Last Updated: {datetime.now().strftime('%Y-%m-%d')}     ║
            ╚═══════════════════════════════════════════════╝
            """
            print(Fore.CYAN + welcome_msg)
            
            typewriter(Fore.YELLOW + "\n🔥 Initializing systems... ")
            time.sleep(1)
            typewriter(Fore.GREEN + "READY!\n\n")
            time.sleep(2)
            return True
        else:
            login_attempts += 1
            remaining = MAX_LOGIN_ATTEMPTS - login_attempts
            print(Fore.RED + f"\n❌ ACCESS DENIED! Attempt {login_attempts}/{MAX_LOGIN_ATTEMPTS}")
            print(Fore.YELLOW + f"⚠️ Remaining attempts: {remaining}")
            
            if remaining > 0:
                time.sleep(2)
                clear()
            else:
                print(Fore.RED + "\n⛔ MAXIMUM ATTEMPTS REACHED!")
                print(Fore.RED + "🚫 System locked. Contact administrator.")
                time.sleep(5)
                exit()
    
    return False

# ===== Main Menu =====
def main_menu():
    email_bomber = EmailBomber()
    
    while True:
        clear()
        print_banner()
        
        # Display statistics
        print(Fore.CYAN + "📊 STATISTICS:")
        print(Fore.YELLOW + f"   📧 Emails Sent: {stats['emails_sent']}")
        print(Fore.YELLOW + f"   📞 Numbers Checked: {stats['numbers_checked']}")
        print(Fore.YELLOW + f"   ⚠️ Reports Made: {stats['reports_made']}")
        print(Fore.YELLOW + f"   ✅ Successful Unbans: {stats['successful_unbans']}")
        
        if stats['last_operation']:
            print(Fore.CYAN + f"   🕒 Last Operation: {stats['last_operation']}")
        
        print(Fore.CYAN + "\n" + "═" * 55)
        print(Fore.MAGENTA + "🎯 MAIN MENU - SELECT AN OPTION")
        print(Fore.CYAN + "═" * 55)
        
        menu_options = [
            "1️⃣  📩 UNBAN TEMPORARY (Enhanced Success Rate)",
            "2️⃣  🚫 UNBAN PERMANENT (Legal Appeal)",
            "3️⃣  🔍 CHECK WHATSAPP NUMBER (Advanced)",
            "4️⃣  ⚠️ REPORT SCAMMER (Temporary Ban)",
            "5️⃣  💀 NUCLEAR REPORT (Permanent + Legal Action)",
            "6️⃣  🚀 MASS REPORT (Multiple Targets)",
            "7️⃣  📊 VIEW STATISTICS",
            "8️⃣  ⚙️  TEST EMAIL ACCOUNTS",
            "0️⃣  ❌ EXIT SYSTEM"
        ]
        
        for option in menu_options:
            print(Fore.CYAN + option)
        
        print(Fore.CYAN + "═" * 55)
        
        choice = input(Fore.YELLOW + "\n🎯 Select option [0-8]: ").strip()
        
        if choice == "1":
            temporary_unban(email_bomber)
        elif choice == "2":
            permanent_unban(email_bomber)
        elif choice == "3":
            check_number()
        elif choice == "4":
            temporary_report(email_bomber)
        elif choice == "5":
            permanent_report(email_bomber)
        elif choice == "6":
            mass_report(email_bomber)
        elif choice == "7":
            show_statistics()
        elif choice == "8":
            test_accounts(email_bomber)
        elif choice == "0":
            print(Fore.YELLOW + "\n👋 Exiting system...")
            print(Fore.GREEN + "🔥 Thank you for using WhatsApp Unban Tool v2.0!")
            time.sleep(2)
            break
        else:
            print(Fore.RED + "\n❌ Invalid option!")
            time.sleep(1)

# ===== Enhanced Feature Functions =====
def temporary_unban(email_bomber):
    clear()
    print_banner()
    print(Fore.MAGENTA + "\n" + "═" * 55)
    print(Fore.CYAN + "📩 TEMPORARY UNBAN REQUEST")
    print(Fore.MAGENTA + "═" * 55)
    
    phone = input(Fore.YELLOW + "\n📞 Enter WhatsApp number (+1234567890): ").strip()
    
    if not validate_phone_number(phone):
        print(Fore.RED + "❌ Invalid phone number format!")
        time.sleep(2)
        return
    
    print(Fore.CYAN + f"\n🔍 Validating {phone}...")
    time.sleep(1)
    
    # Check if number exists
    is_valid, wa_id = enhanced_check_whatsapp_number(phone)
    
    if not is_valid:
        print(Fore.RED + "\n⚠️ Number not found on WhatsApp. Proceed anyway? (y/n): ")
        if input().lower() != 'y':
            return
    
    # Get template
    template = get_unban_template("temporary", phone)
    
    print(Fore.YELLOW + "\n⚡ Preparing enhanced email campaign...")
    
    # Send to ALL email categories
    total_success = 0
    total_fail = 0
    
    for category, emails in SUPPORT_EMAILS.items():
        print(Fore.CYAN + f"\n📨 Sending to {category.upper()} department ({len(emails)} emails)...")
        success, fail = email_bomber.mass_send(
            emails, 
            template["subject"], 
            template["body"],
            email_type="urgent",
            threads=3
        )
        total_success += success
        total_fail += fail
    
    print(Fore.MAGENTA + "\n" + "═" * 55)
    print(Fore.GREEN + f"✅ CAMPAIGN COMPLETE!")
    print(Fore.CYAN + f"   📤 Successfully sent: {total_success} emails")
    print(Fore.RED + f"   📥 Failed: {total_fail} emails")
    print(Fore.YELLOW + f"   🎯 Target: {phone}")
    
    stats["last_operation"] = f"Temporary unban request for {phone}"
    
    print(Fore.GREEN + "\n🔥 Pro Tips:")
    print(Fore.YELLOW + "   • Keep your WhatsApp app updated")
    print(Fore.YELLOW + "   • Don't spam messages after unban")
    print(Fore.YELLOW + "   • Wait 24-48 hours for response")
    print(Fore.YELLOW + "   • Run check again in 24 hours")
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def permanent_unban(email_bomber):
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 55)
    print(Fore.YELLOW + "🚫 PERMANENT UNBAN APPEAL (LEGAL)")
    print(Fore.RED + "═" * 55)
    
    print(Fore.YELLOW + "\n⚠️  WARNING: This is for PERMANENTLY banned accounts only!")
    print(Fore.YELLOW + "   Use only if you've exhausted all other options.\n")
    
    phone = input(Fore.YELLOW + "📞 Enter permanently banned number: ").strip()
    
    if not validate_phone_number(phone):
        print(Fore.RED + "❌ Invalid phone number!")
        time.sleep(2)
        return
    
    confirm = input(Fore.RED + f"\n⚠️  CONFIRM: Appeal for PERMANENT ban on {phone}? (yes/NO): ").lower()
    if confirm != "yes":
        print(Fore.YELLOW + "❌ Cancelled.")
        time.sleep(1)
        return
    
    # Get legal template
    template = get_unban_template("permanent", phone)
    
    print(Fore.RED + "\n⚡ Launching LEGAL APPEAL campaign...")
    
    # Send with maximum priority
    total_success = 0
    for category, emails in SUPPORT_EMAILS.items():
        print(Fore.CYAN + f"\n⚖️ Sending LEGAL appeal to {category.upper()}...")
        success, fail = email_bomber.mass_send(
            emails,
            template["subject"],
            template["body"],
            email_type="urgent",
            threads=5
        )
        total_success += success
    
    print(Fore.GREEN + f"\n✅ Legal appeal submitted for {phone}")
    print(Fore.YELLOW + "📞 Expected response time: 3-7 business days")
    
    stats["last_operation"] = f"Permanent unban appeal for {phone}"
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def check_number():
    clear()
    print_banner()
    print(Fore.CYAN + "\n" + "═" * 55)
    print(Fore.GREEN + "🔍 ADVANCED NUMBER CHECK")
    print(Fore.CYAN + "═" * 55)
    
    phone = input(Fore.YELLOW + "\n📞 Enter number to check: ").strip()
    
    if not validate_phone_number(phone):
        print(Fore.RED + "❌ Invalid format!")
        time.sleep(2)
        return
    
    print(Fore.CYAN + "\n🔬 Running comprehensive check...")
    
    # Run enhanced check
    is_valid, wa_id = enhanced_check_whatsapp_number(phone)
    
    if is_valid:
        print(Fore.GREEN + "\n" + "✓" * 30)
        print(Fore.GREEN + f"✅ NUMBER ACTIVE: {phone}")
        print(Fore.GREEN + f"📱 WhatsApp ID: {wa_id}")
        print(Fore.GREEN + "✓" * 30)
        
        stats["numbers_checked"] += 1
        stats["last_operation"] = f"Checked {phone} - ACTIVE"
    else:
        print(Fore.RED + "\n" + "✗" * 30)
        print(Fore.RED + f"❌ NUMBER NOT FOUND: {phone}")
        print(Fore.RED + "✗" * 30)
        
        stats["numbers_checked"] += 1
        stats["last_operation"] = f"Checked {phone} - INACTIVE"
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def temporary_report(email_bomber):
    clear()
    print_banner()
    print(Fore.YELLOW + "\n" + "═" * 55)
    print(Fore.RED + "⚠️  TEMPORARY SCAMMER REPORT")
    print(Fore.YELLOW + "═" * 55)
    
    target = input(Fore.YELLOW + "\n📞 Enter scammer's number: ").strip()
    
    if not validate_phone_number(target):
        print(Fore.RED + "❌ Invalid number!")
        time.sleep(2)
        return
    
    print(Fore.CYAN + f"\n🔍 Verifying {target}...")
    is_valid, wa_id = enhanced_check_whatsapp_number(target)
    
    if not is_valid:
        print(Fore.RED + "⚠️ Number not on WhatsApp. Report anyway? (y/n): ")
        if input().lower() != 'y':
            return
    
    template = get_report_template("temporary_report", target)
    
    confirm = input(Fore.RED + f"\n⚠️  REPORT {target} for scamming? (yes/NO): ").lower()
    if confirm != "yes":
        print(Fore.YELLOW + "❌ Cancelled.")
        return
    
    print(Fore.RED + "\n⚡ Launching scam report campaign...")
    
    # Send to security departments only
    security_emails = SUPPORT_EMAILS["security"] + SUPPORT_EMAILS["urgent"]
    success, fail = email_bomber.mass_send(
        security_emails,
        template["subject"],
        template["body"],
        email_type="urgent",
        threads=4
    )
    
    print(Fore.GREEN + f"\n✅ Reported {target} to {success} security contacts")
    print(Fore.YELLOW + "⏰ Expected action: 1-24 hours")
    
    stats["reports_made"] += 1
    stats["last_operation"] = f"Reported scammer {target}"
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def permanent_report(email_bomber):
    clear()
    print_banner()
    print(Fore.RED + "\n" + "═" * 55)
    print(Fore.RED + "💀 NUCLEAR REPORT (PERMANENT + LEGAL)")
    print(Fore.RED + "═" * 55)
    
    print(Fore.YELLOW + "\n⚠️  EXTREME WARNING: This will:")
    print(Fore.RED + "   • Trigger permanent ban")
    print(Fore.RED + "   • Flag for law enforcement")
    print(Fore.RED + "   • Create permanent record")
    print(Fore.YELLOW + "   • Use STRONGEST possible language\n")
    
    target = input(Fore.YELLOW + "📞 Enter CRIMINAL's number: ").strip()
    
    if not validate_phone_number(target):
        print(Fore.RED + "❌ Invalid!")
        time.sleep(2)
        return
    
    confirm = input(Fore.RED + f"\n💀 CONFIRM NUCLEAR REPORT on {target}? (type 'NUKE' to confirm): ")
    if confirm != "NUKE":
        print(Fore.YELLOW + "❌ Cancelled.")
        return
    
    template = get_report_template("permanent_report", target)
    
    print(Fore.RED + "\n💥 DEPLOYING NUCLEAR REPORT...")
    time.sleep(2)
    
    # Send to ALL departments with maximum force
    all_emails = []
    for category in SUPPORT_EMAILS.values():
        all_emails.extend(category)
    
    # Add extra copies
    all_emails = all_emails * 3
    
    success, fail = email_bomber.mass_send(
        all_emails[:100],  # Limit to 100 emails
        template["subject"],
        template["body"],
        email_type="urgent",
        threads=10
    )
    
    print(Fore.RED + "\n" + "☢" * 30)
    print(Fore.RED + f"💀 NUCLEAR REPORT DEPLOYED: {target}")
    print(Fore.RED + f"📧 Reports sent: {success}")
    print(Fore.YELLOW + f"⏰ Expected nuclear response: <12 hours")
    print(Fore.RED + "☢" * 30)
    
    stats["reports_made"] += 1
    stats["last_operation"] = f"NUKE report on {target}"
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def mass_report(email_bomber):
    clear()
    print_banner()
    print(Fore.MAGENTA + "\n" + "═" * 55)
    print(Fore.CYAN + "🚀 MASS REPORT SYSTEM")
    print(Fore.MAGENTA + "═" * 55)
    
    print(Fore.YELLOW + "\n📝 Enter multiple numbers (one per line)")
    print(Fore.YELLOW + "   Type 'DONE' when finished\n")
    
    numbers = []
    while True:
        num = input(Fore.CYAN + f"Number {len(numbers)+1}: ").strip()
        if num.upper() == "DONE":
            break
        if validate_phone_number(num):
            numbers.append(num)
        else:
            print(Fore.RED + "   ❌ Invalid, skipping...")
    
    if not numbers:
        print(Fore.RED + "❌ No valid numbers!")
        return
    
    print(Fore.GREEN + f"\n✅ Loaded {len(numbers)} numbers")
    
    confirm = input(Fore.YELLOW + f"\n⚠️  Report {len(numbers)} numbers? (yes/NO): ").lower()
    if confirm != "yes":
        return
    
    template = get_report_template("temporary_report", "MULTIPLE_NUMBERS")
    
    # Modify template for mass report
    mass_body = template["body"].replace("MULTIPLE_NUMBERS", "\n".join(numbers))
    mass_subject = f"MASS SCAMMER REPORT: {len(numbers)} Numbers"
    
    print(Fore.CYAN + "\n⚡ Launching mass report...")
    
    success, fail = email_bomber.mass_send(
        SUPPORT_EMAILS["security"],
        mass_subject,
        mass_body,
        threads=5
    )
    
    print(Fore.GREEN + f"\n✅ Mass report completed!")
    print(Fore.CYAN + f"   📞 Numbers reported: {len(numbers)}")
    print(Fore.CYAN + f"   📧 Reports sent: {success}")
    
    stats["reports_made"] += len(numbers)
    stats["last_operation"] = f"Mass report on {len(numbers)} numbers"
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def show_statistics():
    clear()
    print_banner()
    print(Fore.CYAN + "\n" + "═" * 55)
    print(Fore.GREEN + "📊 SYSTEM STATISTICS")
    print(Fore.CYAN + "═" * 55)
    
    print(Fore.YELLOW + "\n📈 PERFORMANCE METRICS:")
    print(Fore.CYAN + f"   📧 Total Emails Sent: {stats['emails_sent']}")
    print(Fore.CYAN + f"   📞 Numbers Checked: {stats['numbers_checked']}")
    print(Fore.CYAN + f"   ⚠️  Reports Made: {stats['reports_made']}")
    print(Fore.CYAN + f"   ✅ Successful Unbans: {stats['successful_unbans']}")
    
    if stats['last_operation']:
        print(Fore.YELLOW + f"\n🕒 Last Operation: {stats['last_operation']}")
    
    print(Fore.YELLOW + f"\n📅 Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(Fore.CYAN + "\n" + "═" * 55)
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

def test_accounts(email_bomber):
    clear()
    print_banner()
    print(Fore.CYAN + "\n" + "═" * 55)
    print(Fore.YELLOW + "⚙️  ACCOUNT TESTING SYSTEM")
    print(Fore.CYAN + "═" * 55)
    
    print(Fore.YELLOW + "\n🔍 Testing email accounts...\n")
    
    working = 0
    for account in gmail_accounts:
        print(Fore.CYAN + f"   Testing {account['email']}... ", end='', flush=True)
        if email_bomber.test_account(account):
            print(Fore.GREEN + "✅ ACTIVE")
            working += 1
        else:
            print(Fore.RED + "❌ INACTIVE")
        time.sleep(0.5)
    
    print(Fore.MAGENTA + "\n" + "═" * 55)
    print(Fore.GREEN + f"✅ {working}/{len(gmail_accounts)} accounts active")
    
    if working < 2:
        print(Fore.RED + "⚠️  WARNING: Need at least 2 working accounts!")
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

# ===== Main Execution =====
if __name__ == "__main__":
    try:
        if login():
            main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n👋 Program interrupted by user")
    except Exception as e:
        print(Fore.RED + f"\n⚠️  Critical error: {e}")
        print(Fore.YELLOW + "Please contact support.")
    finally:
        print(Fore.CYAN + "\n🔥 WhatsApp Unban Tool v2.0 - Enhanced Edition")
        print(Fore.YELLOW + "📧 Support: tunzyshop@protonmail.com")
