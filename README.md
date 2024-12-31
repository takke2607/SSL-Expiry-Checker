# SSL-Expiry-Checker

SSL Expiry Checker is a simple Python-based tool that helps you monitor SSL certificate expiry dates for multiple domains. It checks the expiration status of certificates and sends email notifications if a certificate is about to expire or has already expired. This tool is ideal for administrators and security teams to ensure timely renewal of SSL certificates, preventing potential security risks due to expired certificates.

Key Features:
Monitors SSL certificate expiry for domains.
Sends email notifications for soon-to-expire or expired certificates.
Configurable threshold for when to send notifications.
Simple to use with domain list input and recipient configuration.

Steps to Run the Tool:

Clone the Repository: Clone the repository to your local machine using Git:
git clone https://github.com/yourusername/ssl-expiry-checker.git

Install Dependencies: Install required Python libraries using pip:
pip install -r requirements.txt

Configure Domains and Recipients:
In the file named domains.txt add the domains you want to monitor, one per line.
In the file named recipients.txt add the email addresses where notifications should be sent, one per line.
Set Notification Threshold: In the script, adjust the NOTIFY_DAYS_THRESHOLD value to set the number of days before certificate expiry to trigger a notification (e.g., NOTIFY_DAYS_THRESHOLD = 15).

Run the Script: Execute the script to check the SSL expiry dates:
python ssl_expiry_checker.py

Receive Notifications: If any SSL certificates are expired or about to expire based on the threshold, an email notification will be sent to the recipients listed in recipients.txt.
