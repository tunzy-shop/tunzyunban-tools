import os
import time
import re
import random
import getpass
from colorama import Fore, Style, init

init(autoreset=True)

# ===== Authentication =====
tool_username = "tunzy"
tool_password = "tunzyban"

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
    """Validate phone number format"""
    return bool(re.match(r'^\+\d{10,15}$', phone))

# ===== Appeal Templates =====
def generate_ban_report(phone, ban_type):
    """Generate a ban report for scammers"""
    
    if ban_type == "temporary":
        return f"""
**URGENT REPORT: Temporary Ban Required**

Account Information:
• Phone Number: {phone}
• Violation Type: Active Scamming/Fraud
• Recommended Action: 30-day suspension

Violations Detected:
1. Financial fraud targeting elderly victims
2. Impersonation of official accounts
3. Fake investment schemes
4. Harassment and threats to users

Evidence Available:
• Multiple victim complaints
• Fraudulent message patterns
• Fake identity documentation
• Financial transaction records

Request: Please temporarily suspend this account for investigation.
"""
    else:  # permanent ban
        return f"""
**CRITICAL REPORT: Permanent Ban Required**

Account Information:
• Phone Number: {phone}
• Violation Type: Serial Criminal Activity
• Recommended Action: Permanent termination

Confirmed Criminal Activities:
1. Organized fraud network operations
2. Identity theft and impersonation
3. Child exploitation material distribution
4. Terror financing connections
5. Death threats to victims

Law Enforcement Involvement:
• Multiple police investigations active
• INTERPOL references available
• Financial crime unit coordination
• Victim protection program needed

Request: Permanently ban this account and preserve all data for prosecution.
"""

def generate_unban_appeal(phone, ban_type, user_name, reason):
    """Generate an unban appeal for wrongfully banned users"""
    
    if ban_type == "temporary":
        return f"""
**Formal Appeal: Temporary Ban Reversal**

Account Information:
• Phone Number: {phone}
• Account Holder: {user_name}
• Ban Type: Temporary
• Appeal Reason: {reason}

Appeal Details:
I believe my account was wrongfully suspended due to:
1. Automated system false positive
2. Mass false reporting by competitors
3. Technical error during system update
4. Identity confusion with similar number

Account History:
• {random.randint(1, 8)}+ years of legitimate use
• Zero previous violations
• Regular personal/business communication
• Verified identity available upon request

Impact of Suspension:
• Business operations disrupted
• Family emergency communications blocked
• Financial transactions halted
• Reputation damage occurring

Request: Please review my account and lift the temporary suspension.

Sincerely,
{user_name}
Phone: {phone}
"""
    else:  # permanent ban appeal
        return f"""
**Legal Appeal: Permanent Ban Reversal**

Account Information:
• Phone Number: {phone}
• Account Holder: {user_name}
• Ban Type: Permanent
• Appeal Reason: {reason}

Formal Appeal Statement:
My account has been permanently banned in error due to:

1. Identity theft (someone impersonated me)
2. Catastrophic system failure
3. Fabricated evidence accepted without verification
4. Complete failure of due process

Evidence of Error:
• Location proof: I was overseas when "violations" occurred
• Device logs showing legitimate usage patterns
• Character references from reputable sources
• Government ID verification available

Severe Damages Incurred:
• Business destruction: ${random.randint(10000, 50000)}+ losses
• Client relationships permanently damaged
• Personal reputation destroyed
• Emotional trauma documented

Legal Grounds for Reversal:
• Breach of WhatsApp Terms of Service
• Negligent infliction of economic loss
• Defamation (false criminal labeling)
• Failure of due process

DEMAND: Full account restoration within 48 hours.

{user_name}
Phone: {phone}
Legal Representation: Retained
"""

# ===== Official Appeal Guide =====
def show_official_guide(ban_type):
    """Show official WhatsApp appeal process"""
    
    print(Fore.CYAN + "\n" + "═" * 50)
    print(Fore.YELLOW + "📋 OFFICIAL WHATSAPP APPEAL GUIDE")
    print(Fore.CYAN + "═" * 50)
    
    if ban_type == "unban":
        guide = """
OFFICIAL STEPS TO UNBAN YOUR ACCOUNT:

1. CHECK BAN TYPE IN THE APP
   • Open WhatsApp, see if it shows "temporary" or "permanent" ban
   • Temporary bans usually last 24-72 hours
   • Permanent bans require formal appeal

2. UNINSTALL UNOFFICIAL APPS
   • Remove GB WhatsApp, WhatsApp Plus, etc.
   • Install official WhatsApp from Play Store/App Store

3. SUBMIT APPEAL THROUGH OFFICIAL CHANNEL
   • In the ban screen, tap "Support" or "Request a review"
   • Use the appeal message generated by this tool
   • Include your full phone number with country code

4. WAIT FOR RESPONSE
   • Response time: 24-72 hours for temporary bans
   • Response time: 3-7 days for permanent bans
   • DO NOT submit multiple appeals (slows process)

5. KEY TO SUCCESS:
   • Be polite and truthful in your appeal
   • Provide clear explanations
   • Accept responsibility if you violated rules
   • Show willingness to follow guidelines
"""
    else:  # ban guide
        guide = """
HOW TO REPORT SCAMMERS OFFICIALLY:

1. IN-APP REPORTING (Most Effective)
   • Open chat with the scammer
   • Tap their name → Report → Select reason
   • Choose "Block and Report"

2. EMAIL REPORTING (For Serious Cases)
   • Email: support@support.whatsapp.com
   • Include: Scammer's phone number
   • Include: Screenshots of fraudulent messages
   • Include: Description of the scam

3. PROVIDE EVIDENCE
   • Screenshots of conversations
   • Transaction records if money was sent
   • Details of the scam method
   • Number of victims affected

4. FOLLOW UP
   • Wait 24-48 hours for initial response
   • Provide additional evidence if requested
   • Report to local authorities for serious fraud
"""
    
    print(Fore.WHITE + guide)
    print(Fore.CYAN + "═" * 50)
    input(Fore.YELLOW + "\nPress Enter to continue...")

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
    while True:
        clear()
        print_banner()
        
        print(Fore.CYAN + "\n" + "─" * 30)
        print(Fore.YELLOW + "🎯 CONTROL PANEL")
        print(Fore.CYAN + "─" * 30)
        
        print(Fore.GREEN + "\n1. GENERATE BAN REPORT")
        print(Fore.GREEN + "2. GENERATE UNBAN APPEAL")
        print(Fore.GREEN + "3. OFFICIAL APPEAL GUIDE")
        print(Fore.RED + "0. EXIT")
        
        print(Fore.CYAN + "─" * 30)
        
        choice = input(Fore.YELLOW + "\nSelect: ").strip()
        
        if choice == "1":
            generate_ban_menu()
        elif choice == "2":
            generate_unban_menu()
        elif choice == "3":
            show_guide_menu()
        elif choice == "0":
            print(Fore.YELLOW + "\n👋 Exiting...")
            break
        else:
            print(Fore.RED + "\n❌ Invalid!")
            time.sleep(1)

def generate_ban_menu():
    clear()
    print_banner()
    
    print(Fore.CYAN + "\n" + "─" * 30)
    print(Fore.YELLOW + "🚫 BAN REPORT GENERATOR")
    print(Fore.CYAN + "─" * 30)
    
    # Select ban type
    print(Fore.GREEN + "\n1. TEMPORARY BAN REPORT")
    print(Fore.GREEN + "2. PERMANENT BAN REPORT")
    
    ban_choice = input(Fore.YELLOW + "\nSelect ban type: ").strip()
    
    if ban_choice == "1":
        ban_type = "temporary"
    elif ban_choice == "2":
        ban_type = "permanent"
    else:
        print(Fore.RED + "\n❌ Invalid choice!")
        time.sleep(1)
        return
    
    # Get phone number
    phone = input(Fore.YELLOW + f"\nEnter scammer's phone number: ").strip()
    
    if not validate_phone(phone):
        print(Fore.RED + "\n❌ Invalid phone number format!")
        print(Fore.YELLOW + "Use format: +1234567890")
        time.sleep(2)
        return
    
    # Generate report
    clear()
    print_banner()
    print(Fore.GREEN + f"\n✅ GENERATING {ban_type.upper()} BAN REPORT")
    print(Fore.CYAN + "─" * 50)
    
    report = generate_ban_report(phone, ban_type)
    print(Fore.WHITE + report)
    
    print(Fore.CYAN + "─" * 50)
    print(Fore.YELLOW + "\n📋 HOW TO USE THIS REPORT:")
    print(Fore.WHITE + "1. Copy the report above")
    print(Fore.WHITE + f"2. Email to: support@support.whatsapp.com")
    print(Fore.WHITE + "3. Include screenshots as evidence")
    print(Fore.WHITE + "4. Wait 24-48 hours for response")
    
    # Save to file option
    save = input(Fore.YELLOW + "\nSave to file? (y/n): ").lower()
    if save == 'y':
        filename = f"ban_report_{phone.replace('+', '')}.txt"
        with open(filename, 'w') as f:
            f.write(report)
        print(Fore.GREEN + f"✅ Report saved as {filename}")
    
    input(Fore.CYAN + "\nPress Enter to continue...")

def generate_unban_menu():
    clear()
    print_banner()
    
    print(Fore.CYAN + "\n" + "─" * 30)
    print(Fore.YELLOW + "✅ UNBAN APPEAL GENERATOR")
    print(Fore.CYAN + "─" * 30)
    
    # Select ban type
    print(Fore.GREEN + "\n1. TEMPORARY BAN APPEAL")
    print(Fore.GREEN + "2. PERMANENT BAN APPEAL")
    
    ban_choice = input(Fore.YELLOW + "\nWhat type of ban?: ").strip()
    
    if ban_choice == "1":
        ban_type = "temporary"
    elif ban_choice == "2":
        ban_type = "permanent"
    else:
        print(Fore.RED + "\n❌ Invalid choice!")
        time.sleep(1)
        return
    
    # Get user information
    print(Fore.CYAN + "\n" + "─" * 30)
    print(Fore.YELLOW + "📝 USER INFORMATION")
    print(Fore.CYAN + "─" * 30)
    
    phone = input(Fore.YELLOW + "\nYour phone number: ").strip()
    
    if not validate_phone(phone):
        print(Fore.RED + "\n❌ Invalid phone number format!")
        print(Fore.YELLOW + "Use format: +1234567890")
        time.sleep(2)
        return
    
    name = input(Fore.YELLOW + "Your name: ").strip()
    
    print(Fore.GREEN + "\nSelect appeal reason:")
    print(Fore.WHITE + "1. False positive / Automated system error")
    print(Fore.WHITE + "2. Mass false reporting by others")
    print(Fore.WHITE + "3. Identity confusion / Someone impersonated me")
    print(Fore.WHITE + "4. Technical error during update")
    print(Fore.WHITE + "5. I apologize for unintentional violation")
    
    reason_choice = input(Fore.YELLOW + "\nSelect reason (1-5): ").strip()
    
    reasons = {
        "1": "False positive / Automated system error",
        "2": "Mass false reporting by others",
        "3": "Identity confusion / Someone impersonated me",
        "4": "Technical error during update",
        "5": "Apology for unintentional violation"
    }
    
    reason = reasons.get(reason_choice, "Appeal for account review")
    
    # Generate appeal
    clear()
    print_banner()
    print(Fore.GREEN + f"\n✅ GENERATING {ban_type.upper()} UNBAN APPEAL")
    print(Fore.CYAN + "─" * 50)
    
    appeal = generate_unban_appeal(phone, ban_type, name, reason)
    print(Fore.WHITE + appeal)
    
    print(Fore.CYAN + "─" * 50)
    print(Fore.YELLOW + "\n📋 HOW TO SUBMIT THIS APPEAL:")
    print(Fore.WHITE + "1. Copy the entire appeal above")
    print(Fore.WHITE + "2. Open WhatsApp on your banned phone")
    print(Fore.WHITE + "3. When ban screen appears, tap 'Support'")
    print(Fore.WHITE + "4. Paste the appeal in the message field")
    print(Fore.WHITE + "5. Submit and wait for response")
    
    if ban_type == "temporary":
        print(Fore.GREEN + "\n⏰ Expected response: 24-72 hours")
    else:
        print(Fore.GREEN + "\n⏰ Expected response: 3-7 days")
    
    # Save to file option
    save = input(Fore.YELLOW + "\nSave to file? (y/n): ").lower()
    if save == 'y':
        filename = f"unban_appeal_{phone.replace('+', '')}.txt"
        with open(filename, 'w') as f:
            f.write(appeal)
        print(Fore.GREEN + f"✅ Appeal saved as {filename}")
    
    input(Fore.CYAN + "\nPress Enter to continue...")

def show_guide_menu():
    clear()
    print_banner()
    
    print(Fore.CYAN + "\n" + "─" * 30)
    print(Fore.YELLOW + "📚 OFFICIAL GUIDES")
    print(Fore.CYAN + "─" * 30)
    
    print(Fore.GREEN + "\n1. UNBAN APPEAL GUIDE")
    print(Fore.GREEN + "2. BAN REPORTING GUIDE")
    
    choice = input(Fore.YELLOW + "\nSelect guide: ").strip()
    
    if choice == "1":
        show_official_guide("unban")
    elif choice == "2":
        show_official_guide("ban")
    else:
        print(Fore.RED + "\n❌ Invalid choice!")
        time.sleep(1)

# ===== Main Program =====
if __name__ == "__main__":
    try:
        if login():
            main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n👋 Program stopped")
    except Exception as e:
        print(Fore.RED + f"\n⚠️  Error: {str(e)[:50]}")
    finally:
        print(Fore.CYAN + "\n" + "─" * 30)
        print(Fore.YELLOW + "VENOM STRIKE")
        print(Fore.GREEN + "BY TUNZY SHOP")
        print(Fore.CYAN + "─" * 30)