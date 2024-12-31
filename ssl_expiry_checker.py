import ssl
import socket
import datetime
import subprocess
import os

# Configurable threshold for days before certificate expiration to send notification
NOTIFY_DAYS_THRESHOLD = 15  # Change this value for testing different thresholds

def send_email(domain, subject, body, recipients_file):
    """Helper function to send email."""
    try:
        # Check if recipients file exists
        if not os.path.exists(recipients_file):
            print(f"[ERROR] Recipients file '{recipients_file}' not found.")
            return

        with open("mailbody.txt", "w") as body_file:
            body_file.write(body)

        with open(recipients_file, "r") as recipients_input_file:
            recipients = recipients_input_file.read().splitlines()

        if not recipients:
            print(f"[ERROR] No recipients found in '{recipients_file}'.")
            return

        with open("recipients.txt", "w") as recipients_output_file:
            for recipient in recipients:
                recipients_output_file.write(f"{recipient}\n")

        # Run the mailsend script (ensure it's correct and executable)
        result = subprocess.run(["python3", "mailsend.py", "recipients.txt", "mailbody.txt", subject], capture_output=True)
        
        if result.returncode != 0:
            print(f"[ERROR] Email sending failed for {domain}: {result.stderr.decode()}")
        else:
            print(f"[INFO] Email sent successfully for {domain}.")
    except Exception as e:
        print(f"[ERROR] Failed to send email for {domain}: {e}")

def check_ssl_expiry(domain, port=443, recipients_file="recipients.txt"):
    try:
        # Split the domain and port if a custom port is provided
        if ":" in domain:
            domain, port = domain.split(":")
            port = int(port)
        else:
            port = 443

        # Create a socket connection to the domain
        context = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                ssl_info = ssock.getpeercert()

        # Get the certificate expiration date
        expiry_date_str = ssl_info['notAfter']
        expiry_date = datetime.datetime.strptime(expiry_date_str, "%b %d %H:%M:%S %Y %Z")

        # Calculate days remaining
        days_remaining = (expiry_date - datetime.datetime.utcnow()).days

        # Format output
        print("="*70)
        print(f"SSL Certificate Expiry Check - {domain}")
        print("-"*70)
        print(f"Certificate Expiry Date: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Days Remaining: {days_remaining} days")

        # Check expiration status and send email if expired or expiring soon
        if days_remaining < 0:
            subject = f"ALERT: SSL Certificate for {domain} Has Expired"
            body = f"Critical: The SSL certificate for {domain} expired on {expiry_date.strftime('%Y-%m-%d %H:%M:%S')}. Please renew it immediately."
            send_email(domain, subject, body, recipients_file)
        elif days_remaining <= NOTIFY_DAYS_THRESHOLD:
            subject = f"ALERT: SSL Certificate for {domain} Expiring Soon"
            body = f"Warning: The SSL certificate for {domain} will expire on {expiry_date.strftime('%Y-%m-%d %H:%M:%S')} ({days_remaining} days remaining). Please renew it as soon as possible."
            send_email(domain, subject, body, recipients_file)
        elif days_remaining < 30:
            print(f"[WARNING] The SSL certificate for {domain} will expire in {days_remaining} days.")
        else:
            print(f"[INFO] The SSL certificate for {domain} is valid and has {days_remaining} days remaining.")

        print("="*70 + "\n")

    except ssl.SSLCertVerificationError as e:
        print(f"[ERROR] SSL Certificate Verification Error for {domain}: {e}")
        subject = f"ALERT: SSL Certificate for {domain} Has Expired"
        body = f"Critical: The SSL certificate for {domain} has expired. Immediate renewal is required."
        send_email(domain, subject, body, recipients_file)
    except socket.error as e:
        print(f"[ERROR] Could not connect to {domain}: {e}")
        subject = f"ALERT: Unable to Connect to {domain}"
        body = f"Error: Unable to connect to {domain}. Please check the server status and network connectivity."
        send_email(domain, subject, body, recipients_file)
    except Exception as e:
        print(f"[ERROR] Could not check SSL certificate for {domain}: {e}")

# Function to read the domain list from a file
def read_domains_from_file(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"[ERROR] Domain file '{file_path}' not found.")
            return []
        
        with open(file_path, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
        return domains
    except Exception as e:
        print(f"[ERROR] Failed to read domain file: {e}")
        return []

# Path to the file containing domains
file_path = 'domains.txt'  # Replace with the actual path to your file

# Read domains from the file
domains = read_domains_from_file(file_path)

# Check SSL expiry for each domain
if domains:
    for domain in domains:
        check_ssl_expiry(domain, recipients_file="recipients.txt")
else:
    print("[ERROR] No domains to check.")
