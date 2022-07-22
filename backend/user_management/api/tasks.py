import os
from O365 import Account
from dotenv import load_dotenv
from django.conf import settings
from django.utils import timezone

load_dotenv(os.path.join(settings.BASE_DIR, ".env"))


def send_email_activate(first_name, username, email, activation_link):
    credentials = (os.getenv("ONEDRIVE_CLIENT"), os.getenv("ONEDRIVE_SECRET"))
    account = Account(credentials, auth_flow_type="authorization")
    if account.is_authenticated:
        message = account.new_message()
        message.to.add([email])
        message.subject = f"✨ Activate your account, { username } ✨"
        message.body = f"""
            <div>
                👋🏼 Hi { first_name },
                <p>Your account is inactive and requires activation, please click on the button.</p>

                <p>
                    <a
                        href="{ activation_link }"
                        target="_blank"
                        style="
                            border: 2px;
                            color: #fff;
                            width: 150px;
                            font-size: 14px;
                            font-weight: bold;
                            line-height: 32px;
                            text-align: center;
                            border-radius: 8px;
                            display: inline-block;
                            text-decoration: none;
                            background-color: #729ea1;
                        "
                    >
                        Click here
                    </a>
                </p>

                <p>
                    With Regards,<br />
                    National Supercomputing Mission
                </p>
            </div>
        """
        try:
            response = message.send()
            if response:
                return "Mail sent"
            return "Mail couldn't be sent"
        except Exception as e:
            print(e.message)
            return "Mail couldn't be sent"
    else:
        print("Authentication not done")


def send_email_reset_password(first_name, username, email, link):
    credentials = (os.getenv("ONEDRIVE_CLIENT"), os.getenv("ONEDRIVE_SECRET"))
    account = Account(credentials, auth_flow_type="authorization")
    if account.is_authenticated:
        message = account.new_message()
        message.to.add([email])
        message.subject = f"💪 Reset your password { username }"
        message.body = f"""
            <div>
                Dear { first_name },
                <p>It seems you have forgotten your password, no worries we have enabled this link
                for you to reset your password.
                </p>

                <p>
                    <a
                        href="{ link }"
                        target="_blank"
                        style="
                            border: 2px;
                            color: #fff;
                            width: 150px;
                            font-size: 14px;
                            font-weight: bold;
                            line-height: 32px;
                            text-align: center;
                            border-radius: 8px;
                            display: inline-block;
                            text-decoration: none;
                            background-color: #729ea1;
                        "
                    >
                        Click here
                    </a>
                </p>

                <p>
                    With Regards,<br />
                    National Supercomputing Mission
                </p>
            </div>
        """
        try:
            response = message.send()
            if response:
                return "Mail sent"
            return "Mail couldn't be sent"
        except Exception as e:
            print(e.message)
            return "Mail couldn't be sent"
    else:
        print("Authentication not done")


def send_email_mail_change_request(first_name, username, old_email, new_email, link):
    credentials = (os.getenv("ONEDRIVE_CLIENT"), os.getenv("ONEDRIVE_SECRET"))
    account = Account(credentials, auth_flow_type="authorization")
    if account.is_authenticated:
        message = account.new_message()
        message.to.add([old_email])
        message.subject = f"🙏🏽👀 Verify mail change, { username }"
        message.body = f"""
            <div>
                Dear { first_name },
                <p>We have received a request to change the mailing address to { new_email },
                please confirm by clicking on the button below</p>

                <p>
                    <a
                        href="{ link }"
                        target="_blank"
                        style="
                            border: 2px;
                            color: #fff;
                            width: 150px;
                            font-size: 14px;
                            font-weight: bold;
                            line-height: 32px;
                            text-align: center;
                            border-radius: 8px;
                            display: inline-block;
                            text-decoration: none;
                            background-color: #729ea1;
                        "
                    >
                        Click here
                    </a>
                </p>

                <p>
                    With Regards,<br />
                    National Supercomputing Mission
                </p>
            </div>
        """
        try:
            response = message.send()
            if response:
                return "Mail sent"
            return "Mail couldn't be sent"
        except Exception as e:
            print(e.message)
            return "Mail couldn't be sent"
    else:
        print("Authentication not done")


def send_email_accept_mail(first_name, username, email):
    credentials = (os.getenv("ONEDRIVE_CLIENT"), os.getenv("ONEDRIVE_SECRET"))
    account = Account(credentials, auth_flow_type="authorization")
    if account.is_authenticated:
        message = account.new_message()
        message.to.add([email])
        message.subject = f"👏|🙌 Yay { username }, we have updated your email"
        message.body = f"""
            <div>
                Dear { first_name },
                <p>After verifying the request, we have updated your account and
                now all correspondence will take place in this mail</p>

                <p>
                    With Regards,<br />
                    National Supercomputing Mission
                </p>
            </div>
        """
        try:
            response = message.send()
            if response:
                return "Mail sent"
            return "Mail couldn't be sent"
        except Exception as e:
            print(e.message)
            return "Mail couldn't be sent"
    else:
        print("Authentication not done")
