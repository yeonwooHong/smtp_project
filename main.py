from email_sender import mailer, database, auth
from email_sender.colors import Colors
import getpass
import smtplib

def menu():
    # Display the main menu options for the Email Sender program.
    print("\n" + "-" * 40)

    if auth.current_user:
        print(f"{Colors.GREEN}Logged in as:{Colors.END} {auth.current_user.email}")
    else:
        print(f"{Colors.RED}Not logged in{Colors.END}")

    print("-" * 40)
    print(f"{Colors.BOLD}--- Email Sender ---{Colors.END}")
    print("1. Register")
    print("2. Login")
    print("3. Logout")
    print("4. Send Email")
    print("5. View Sent Emails")
    print("6. View Email by ID")
    print("7. Exit")

def main():
    # Initialize or check the database connection
    database.init_db()

    while True:
        # Display the menu and prompt for user input
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            # direct user to register
            if auth.register() == "registered":
                continue 

        elif choice == "2":
            # direct user to login
            if auth.login() == "logged_in":
                continue  

        elif choice == "3":
            # logout user
            if auth.logout() == "logged_out":
                continue
        
        if choice == "4":
            # check if user is logged in
            if not auth.current_user:
                print("You must be logged in to send an email.")
                continue

            try:
                # collect email details 
                sender = auth.current_user.email
                password = getpass.getpass("Enter your Gmail App Password: ").strip()
                
                # Validate app password is provided
                if not password:
                    print(f"{Colors.RED}Error: App password cannot be empty. Please try again.{Colors.END}\n")
                    continue
                
                # Parse comma-separated input into clean lists (ignore empty entries)
                receivers = [x.strip() for x in input("Enter receiver emails (comma separated): ").split(',') if x.strip()]
                
                # Validate receivers are provided
                if not receivers:
                    print(f"{Colors.RED}Error: At least one receiver email is required.{Colors.END}\n")
                    continue
                
                cc = [x.strip() for x in input("Enter CC emails (comma separated, optional): ").split(',') if x.strip()]
                bcc = [x.strip() for x in input("Enter BCC emails (comma separated, optional): ").split(',') if x.strip()]

                subject = input("Enter subject: ").strip()
                
                # Validate subject is provided
                if not subject:
                    print(f"{Colors.RED}Error: Subject cannot be empty.{Colors.END}\n")
                    continue
                
                body = input("Enter body: ").strip()
                
                # Optional file attachment
                attachment = input("Enter file path (or press Enter to skip): ").strip()
                if not attachment:
                    attachment = None

                # Send the email and save it to the database only if successful
                mailer.send_email(sender, password, receivers, cc, bcc, subject, body, attachment)
                database.save_email(sender, receivers, subject, body, cc, bcc, filename=attachment)
                
            except smtplib.SMTPAuthenticationError:
                # This error is already handled in mailer.py with a detailed message
                print(f"{Colors.RED}Email was not sent. Please check the error message above.{Colors.END}\n")
                continue
            except FileNotFoundError as e:
                print(f"{Colors.RED}Error: Attachment file not found: {e}{Colors.END}\n")
                continue
            except Exception as e:
                # Catch any other unexpected errors
                print(f"{Colors.RED}Unexpected error: {e}{Colors.END}\n")
                continue

        elif choice == "5":
            # check if user is logged in
            if not auth.current_user:
                print("Login required.")
                continue

            # Retrieve and display all sent emails from the database
            emails = database.get_all_emails()
            for email in emails:

                print()
                print("-" * 100)
                print(f"ID:       {email.id}")
                print(f"Sender:   {email.sender}")
                print(f"Receiver: {email.receiver}")
                print(f"CC:       {email.cc}")
                print(f"BCC:      {email.bcc}")
                print(f"Subject:  {email.subject}")
                print(f"Status:   {email.status}")
                print(f"Body:     {email.body}")
                print("-" * 100)

        elif choice == "6":
            # check if user is logged in
            if not auth.current_user:
                print("Login required.")
                continue

            # View email by ID
            try:
                email_id = int(input("Enter the email ID to view: "))
                email = database.get_email_by_id(email_id)
                if email:
                    print()
                    print("-" * 100)
                    print(f"ID:       {email.id}")
                    print(f"Sender:   {email.sender}")
                    print(f"Receiver: {email.receiver}")
                    print(f"CC:       {email.cc}")
                    print(f"BCC:      {email.bcc}")
                    print(f"Subject:  {email.subject}")
                    print(f"Status:   {email.status}")
                    print(f"Body:     {email.body}")
                    print("-" * 100)
                else:
                    print(f"No email found with ID {email_id}")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "7":
            # Exit the program
            print("Goodbye!")
            break
        else:
            # Handle invalid menu choices
            print(f"{Colors.RED}Invalid choice. Try again.{Colors.END}")

# Run the program only if this script is executed directly.
if __name__ == "__main__":
    main()
