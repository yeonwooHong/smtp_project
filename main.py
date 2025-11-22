from email_sender import mailer, database
import getpass

def menu():
    # Display the main menu options for the Email Sender program.
    print("\n--- Email Sender ---")
    print("1. Send Email")
    print("2. View Sent Emails")
    print("3. View Email by ID")
    print("4. Exit")

def main():
    # Initialize or check the database connection
    database.init_db()

    while True:
        # Display the menu and prompt for user input
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            # Collect email details from the user
            sender = input("Enter your email: ")
            password = getpass.getpass("Enter your app password: ")

            # Parse comma-separated input into clean lists (ignore empty entries)
            receivers = [x.strip() for x in input("Enter receiver emails (comma separated): ").split(',') if x.strip()]
            cc = [x.strip() for x in input("Enter CC emails (comma separated, optional): ").split(',') if x.strip()]
            bcc = [x.strip() for x in input("Enter BCC emails (comma separated, optional): ").split(',') if x.strip()]

            subject = input("Enter subject: ")
            body = input("Enter body: ")

            # Optional file attachment
            attachment = input("Enter file path (or press Enter to skip): ").strip()
            if not attachment:
                attachment = None

            # Send the email and save it to the database
            mailer.send_email(sender, password, receivers, cc, bcc, subject, body, attachment)
            database.save_email(sender, receivers, subject, body, cc, bcc, filename=attachment)

        elif choice == "2":
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

        elif choice == "3":
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

        elif choice == "4":
            # Exit the program
            print("Goodbye!")
            break
        else:
            # Handle invalid menu choices
            print("Invalid choice. Try again.")

# Run the program only if this script is executed directly.
if __name__ == "__main__":
    main()
