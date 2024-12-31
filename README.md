
# SSL Expiry Checker

SSL Expiry Checker is a simple Python-based tool that helps you monitor SSL certificate expiry dates for multiple domains. It checks the expiration status of certificates and sends email notifications if a certificate is about to expire or has already expired. This tool is ideal for administrators and security teams to ensure timely renewal of SSL certificates, preventing potential security risks due to expired certificates.

## Key Features:
- Monitors SSL certificate expiry for domains.
- Sends email notifications for soon-to-expire or expired certificates.
- Configurable threshold for when to send notifications.
- Simple to use with domain list input and recipient configuration.

## Steps to Run the Tool:

### 1. Clone the Repository
Clone the repository to your local machine using Git:
```bash
git clone https://github.com/yourusername/ssl-expiry-checker.git
```

### 2. Install Dependencies
Install required Python libraries using pip:
```bash
pip install -r requirements.txt
```

### 3. Configure Domains and Recipients
- Create a file named `domains.txt` in the same directory as the script. List the domains you want to monitor, one per line, like so:
  ```txt
  example.com
  example.org
  ```

- Create a file named `recipients.txt` to specify the email addresses where notifications should be sent, one per line. For example:
  ```txt
  admin1@example.com
  admin2@example.org
  ```

### 4. Set Notification Threshold
In the script, you can adjust the `NOTIFY_DAYS_THRESHOLD` value to set the number of days before certificate expiry to trigger a notification. For example:
```python
NOTIFY_DAYS_THRESHOLD = 30  # Change this value to adjust when the notification is triggered
```
This determines how many days before the certificate expires that you'll get notified.

### 5. Run the Script
Execute the script to check the SSL expiry dates. Ensure that you have Python installed (version 3.x is recommended). In the terminal, navigate to the directory containing the script and run:
```bash
python ssl_expiry_checker.py
```

### 6. Receive Notifications
If any SSL certificates are expired or about to expire based on the threshold set in the script, an email notification will be sent to the recipients listed in `recipients.txt`.

---

## Example Usage:

1. Create and configure `domains.txt` and `recipients.txt`.
2. Run the script using the command:
   ```bash
   python ssl_expiry_checker.py
   ```

The script will check the expiry dates of the SSL certificates for each domain in `domains.txt` and notify the recipients listed in `recipients.txt`.

## License
This tool is open-source and free to use. Feel free to contribute, report issues, or request features.
