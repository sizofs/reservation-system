import re
# Regular Expressions to validate date and time formats

print("Welcome to the Reservation System!")

# Administrator login credentials
admin_username = "admin"
admin_password = "admin123"

# User details and reservations
users = []
reservations = []

# Reservation number counter. The first reservation number is 1.
reservation_number = 1

# Hourly reservation rate
hourly_rate = 1000

# Main menu
while True:
    print("\n--- Main Menu ---")
    print("1. Admin Login")
    print("2. User Login")
    print("3. User Registration")
    selection = input("Your choice: ")

    if selection == "1":
        print("\n--- Admin Login ---")
        username = input("Admin Username: ").strip()
        password = input("Admin Password: ").strip()

        if username == admin_username and password == admin_password:
            print("\nWelcome, Admin!")

            while True:
                print("\n--- Admin Panel ---")
                print("1. View all users")
                print("2. View all reservations")
                print("3. Delete a reservation")
                print("4. Edit users")
                print("5. View total income")
                print("6. Log out")
                sub_selection = input("Your choice: ")

                if sub_selection == "1":
                    print("\n--- All Users ---")
                    if not users:
                        print("No users available.")
                    else:
                        for user in users:
                            print(f"Username: {user[0]}, Password: {user[1]}")

                elif sub_selection == "2":
                    print("\n--- All Reservations ---")
                    if not reservations:
                        print("No reservations available.")
                    else:
                        for reservation in reservations:
                            print(f"Number: {reservation[0]}, User: {reservation[1]}, Date: {reservation[2]}, Time: {reservation[3]} - {reservation[4]}")

                elif sub_selection == "3":
                    print("\n--- Delete Reservation ---")
                    number = input("Enter the reservation number to delete: ")

                    # Deleting reservation by number
                    deleted = False
                    for i in range(len(reservations)):
                        if str(reservations[i][0]) == number:
                            del reservations[i]
                            print(f"Reservation number {number} successfully deleted!")
                            deleted = True
                            break
                    if not deleted:
                        print(f"No reservation found with number {number}.")
                    else:
                        # Update reservation file
                        with open('reservations.txt', 'w', encoding='utf-8') as file:
                            for reservation in reservations:
                                file.write(f"{reservation[0]}, {reservation[1]}, {reservation[2]}, {reservation[3]}, {reservation[4]}\n")

                elif sub_selection == "4":
                    print("\n--- Edit Users ---")
                    if not users:
                        print("No users available.")
                    else:
                        user_to_delete = input("Enter the username to delete: ").strip()
                        user_deleted = False
                        for i, user in enumerate(users):
                            if user[0] == user_to_delete:
                                del users[i]  # Delete user from the list
                                print(f"User {user_to_delete} successfully deleted!")
                                # Delete user's reservations
                                reservations[:] = [res for res in reservations if res[1] != user_to_delete]

                                # Update income
                                total_income = 0
                                for reservation in reservations:
                                    start_time_int = int(reservation[3].replace(".", ""))
                                    end_time_int = int(reservation[4].replace(".", ""))
                                    # If the end time is smaller than the start time, shift to the next day
                                    if end_time_int <= start_time_int:
                                        end_time_int += 2400  # Add 24:00 (next day)

                                    # Calculate the difference in hours
                                    total_hours = (end_time_int - start_time_int) / 100
                                    total_income += total_hours * hourly_rate
                                    print(f"Total income has been updated: {total_income:.2f} TL")

                                # Update user and reservation files
                                with open('users.txt', 'w', encoding='utf-8') as file:
                                    for user in users:
                                        file.write(f"{user[0]}, {user[1]}\n")

                                with open('reservations.txt', 'w', encoding='utf-8') as file:
                                    for reservation in reservations:
                                        file.write(f"{reservation[0]}, {reservation[1]}, {reservation[2]}, {reservation[3]}, {reservation[4]}\n")

                                user_deleted = True
                                break
                        if not user_deleted:
                            print(f"User {user_to_delete} not found.")

                elif sub_selection == "5":
                    print("\n--- Total Income ---")
                    total_income = 0
                    total_reservations = 0

                    for reservation in reservations:
                        start_time_int = int(reservation[3].replace(".", ""))
                        end_time_int = int(reservation[4].replace(".", ""))

                        # If the end time is smaller than the start time, shift to the next day
                        if end_time_int <= start_time_int:
                            end_time_int += 2400  # Add 24:00 (next day)

                        # Calculate the difference in hours
                        total_hours = (end_time_int - start_time_int) / 100
                        total_income += total_hours * hourly_rate
                        total_reservations += 1

                    # Save total income data to file
                    with open('total_income.txt', 'w', encoding='utf-8') as file:
                        file.write(f"Total Reservation Count: {total_reservations}\n")
                        file.write(f"Total Income: {total_income:.2f} TL\n")

                    print("Total income has been saved to file.")
                    print(f"Total Reservation Count: {total_reservations}")
                    print(f"Total Income: {total_income:.2f} TL")

                elif sub_selection == "6":
                    break

                else:
                    print("Invalid selection. Please try again.")

        else:
            print("\nInvalid admin credentials. Login failed.")

    elif selection == "2":
        print("\n--- User Login ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        login_successful = False

        for user in users:
            if user[0] == username and user[1] == password:
                login_successful = True
                break

        if login_successful:
            print(f"\nWelcome, {username}!")
            while True:
                print("\n--- User Menu ---")
                print("1. Make a Reservation")
                print("2. View My Reservations")
                print("3. Cancel My Reservation")
                print("4. Log out")
                sub_selection = input("Your choice: ")

                if sub_selection == "1":
                    print("\n--- Make a Reservation ---")

                    # Validate date input (DD.MM.YYYY format)
                    while True:
                        date = input("Date (DD.MM.YYYY): ")
                        # Check if the date format is valid
                        if re.match(r"^\d{2}\.\d{2}\.\d{4}$", date):
                            break
                        else:
                            print("Invalid date format! Please enter a date in 'DD.MM.YYYY' format.")

                    # Get start and end times
                    while True:
                        start_time = input("Start Time (HH.MM format): ")
                        if re.match(r"^\d{2}\.\d{2}$", start_time):
                            break
                        else:
                            print("Invalid time format! Please enter time in 'HH.MM' format.")

                    while True:
                        end_time = input("End Time (HH.MM format): ")
                        if re.match(r"^\d{2}\.\d{2}$", end_time):
                            break
                        else:
                            print("Invalid time format! Please enter time in 'HH.MM' format.")

                    # Convert times to integer format
                    start_time_int = int(start_time.replace(".", ""))
                    end_time_int = int(end_time.replace(".", ""))

                    # If the end time is smaller than the start time, assume it is the next day
                    if end_time_int <= start_time_int:
                        end_time_int += 2400  # Add 24:00 (next day)

                    total_hours = (end_time_int - start_time_int) / 100
                    total_fee = total_hours * hourly_rate

                    # Check for overlapping reservations
                    reservation_made = False
                    for reservation in reservations:
                        if reservation[2] == date:
                            if (start_time_int >= int(reservation[3].replace(".", "")) and start_time_int < int(reservation[4].replace(".", ""))) or \
                               (end_time_int > int(reservation[3].replace(".", "")) and end_time_int <= int(reservation[4].replace(".", ""))):
                                reservation_made = True
                                break
                    if reservation_made:
                        print("There is another reservation during this time. Please choose a different time.")
                    else:
                        reservations.append((reservation_number, username, date, start_time, end_time))
                        reservation_number += 1
                        print(f"\nReservation successful! Total fee: {total_fee:.2f} TL")

                        # Write reservation information to file
                        with open('reservations.txt', 'a', encoding='utf-8') as file:
                            file.write(f"{reservation_number}, {username}, {date}, {start_time}, {end_time}\n")

                elif sub_selection == "2":
                    print("\n--- My Reservations ---")
                    user_reservations = [res for res in reservations if res[1] == username]
                    if not user_reservations:
                        print("You have no reservations.")
                    else:
                        for reservation in user_reservations:
                            print(f"Reservation No: {reservation[0]}, Date: {reservation[2]}, Time: {reservation[3]} - {reservation[4]}")

                elif sub_selection == "3":
                    print("\n--- Cancel My Reservation ---")
                    reservation_number = input("Enter the reservation number to cancel: ")

                    # Cancel the reservation
                    canceled = False
                    for i, reservation in enumerate(reservations):
                        if str(reservation[0]) == reservation_number and reservation[1] == username:
                            del reservations[i]
                            print(f"Reservation number {reservation_number} successfully canceled!")
                            canceled = True
                            break
                    if not canceled:
                        print(f"Reservation number {reservation_number} not found or it's not your reservation.")
                    else:
                        # Update reservation file
                        with open('reservations.txt', 'w', encoding='utf-8') as file:
                            for reservation in reservations:
                                file.write(f"{reservation[0]}, {reservation[1]}, {reservation[2]}, {reservation[3]}, {reservation[4]}\n")

                elif sub_selection == "4":
                    break
                else:
                    print("Invalid selection. Please try again.")

        else:
            print("\nInvalid username or password. Please try again.")

    elif selection == "3":
        print("\n--- User Registration ---")
        username = input("Username: ").strip()
        if not username:
            print("\nUsername cannot be empty!")
        else:
            password = input("Password: ").strip()
            exists = False
            for user in users:
                if user[0] == username:
                    exists = True
                    break
            if exists:
                print("\nThis username is already taken.")
            else:
                if password.replace(" ", "") == "":
                    print("\nPassword cannot consist only of spaces.")
                elif len(password) < 5:
                    print("\nPassword must be at least 5 characters long.")
                else:
                    users.append((username, password))
                    print("\nRegistration successful! You can now log in.")

                    # Add user to the file
                    with open('users.txt', 'a', encoding='utf-8') as file:
                        file.write(f"{username}, {password}\n")
