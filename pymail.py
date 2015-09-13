import smtplib
import argparse
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def parse_args():
    
    parser = get_parser()
    args = parser.parse_args()

   
    args.html = open(args.html_filename).read()

   
    if args.username is None:
        args.username = raw_input('Gmail username: ')
    print_args(args)
    return args


def get_parser():
    """ Return the parser used to interpret the script arguments."""
    usage = (
        "Script to send an HTML file as an HTML email, using Google's SMTP server."
        "\nExamples:"
        "\n1. Send the contents of testfile.html to harsha"
        "\n$ send_html_email.py harsha@example.com testfile.html"
    )
    epilog = "NB This script requires a Gmail account."

    parser = argparse.ArgumentParser(description=usage, epilog=epilog,
        # maintains raw formatting, instead of wrapping lines automatically
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('recipients', help='The recipient email addresses (space delimited)', nargs='+')
    parser.add_argument('html_filename', help='The HTML file to use as the email body content')
    parser.add_argument('-s', '--sender',
        help='The sender email address (defaults to <do-not-reply@example.com>)',
        default='do-not-reply@example.com'
    )
    parser.add_argument('-u', '--username',
        help=('A valid Gmail user account (used to authenticate against Google\'s SMTP service). '
            'If this argument is not supplied, the user will be prompted to type it in.')
    )
    parser.add_argument('-t', '--title',
        help='The test email subject line (defaults to "Test email")',
        default="Test email"
    )
    parser.add_argument('-p', '--plain',
        help=('The test email plain text content. This script is designed primarily for the '
            'testing of HTML emails, so this text is really just a placeholder, for completeness. '
            'The default is "This is a test email (plain text)."'),
        default="This is a test email (plain text)"
    )
    parser.add_argument('-d', '--debug', action='store_true',
        help=('Use this option to turn on DEBUG for the SMTP server interaction.')
    )
    return parser


def print_args(args):
    """Print out the input arguments."""
    print 'Sending test email to: %s' % args.recipients
    print 'Sending test email from: %s' % args.sender
    print 'Using Gmail account: %s' % args.username


def create_message(args):
    """ Create the email message container from the input args."""

    msg = MIMEMultipart('alternative')
    msg['Subject'] = args.title
    msg['From'] = args.sender
    msg['To'] = ','.join(args.recipients)

    part1 = MIMEText(args.plain, 'plain')
    part2 = MIMEText(args.html, 'html')

    msg.attach(part1)
    msg.attach(part2)
    return msg


def main():

    args = parse_args()
    msg = create_message(args)

    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.set_debuglevel(args.debug)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(args.sender, getpass())
        smtpserver.sendmail(args.sender, args.recipients, msg.as_string())
        print "Message sent to '%s'." % args.recipients
        smtpserver.quit()
    except smtplib.SMTPAuthenticationError as e:
        print "Unable to send message: %s" % e

if __name__ == "__main__":
    main()

