# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
import jinja2
import sendgrid
from sendgrid.helpers.mail.mail import Email
from sendgrid.helpers.mail.mail import Content
from sendgrid.helpers.mail.mail import Mail

def send(t_email):

    template_name = "planR_email"
    templateLoader = jinja2.FileSystemLoader(searchpath="templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    html_template = templateEnv.get_template(template_name + ".html")
    html_to_send = html_template.render()
    
    from_email = 'help.planr@gmail.com'
    to_emails = t_email

    message = Mail(
    from_email,
    to_emails,
    subject='Did you forget your Password?',
    html_content=Content("text/html", html_to_send))

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)