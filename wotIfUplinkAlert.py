import meraki
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from emailCreds import sender_pass, sender_address, receiver_address, orgKey, orgId, netId

dashboard = meraki.DashboardAPI(orgKey)

server = 'smtp.gmail.com'
port = 587

response = dashboard.appliance.getOrganizationApplianceUplinkStatuses(orgId, total_pages='all')

for entry in response:
    if entry["networkId"] == netId:
        for uplink in response[0]["uplinks"]:
            if uplink["status"] != "active":
                upLinkDown = uplink["interface"]
                upLinkStatus = uplink["status"]

                message = MIMEMultipart("alternative")
                message['From'] = sender_address
                message['To'] = receiver_address
                message['Subject'] = "Meraki Uplink Failure Alert"

                mail_content = "Please note that interface " + upLinkDown + " is in " + upLinkStatus + " status"

                message.attach(MIMEText(mail_content, 'plain'))

                session = smtplib.SMTP(server, port)
                session.ehlo()
                session.starttls()
                session.login(sender_address, sender_pass)
                session.sendmail(sender_address, receiver_address, message.as_string())
                session.quit()