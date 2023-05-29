from pyrogram import Client, filters
from google.colab import drive
import subprocess

# Enter your bot token here
BOT_TOKEN = "5752952621:AAGO61IiffzN23YuXyv71fbDztA_ubGM6qo"

app = Client("telegram_bot", api_id=15849735, api_hash="b8105dc4c17419dfd4165ecf1d0bc100", bot_token=BOT_TOKEN)

# Command handler for /mount command
@app.on_message(filters.command("mount"))
def mount_command(client, message):
    # Check if the user is already mounted
    if not drive.is_mounted():
        # Request Gmail and password from the user
        client.send_message(message.chat.id, "Please enter your Gmail:")
        client.register_next_step_handler(message, mount_drive)
    else:
        client.send_message(message.chat.id, "Google Drive is already mounted.")

# Mount Google Drive using the provided credentials
def mount_drive(client, message):
    gmail = message.text
    client.send_message(message.chat.id, "Please enter your password:")
    client.register_next_step_handler(message, mount_drive_password, gmail)

def mount_drive_password(client, message, gmail):
    password = message.text

    # Authenticate and mount Google Drive
    command = f"echo '{password}' | google-drive-ocamlfuse -headless -label my_drive {gmail}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Check if mount was successful
    if "successfully authenticated" in output.decode():
        drive.mount("/content/drive")
        client.send_message(message.chat.id, "Google Drive mounted successfully.")
    else:
        client.send_message(message.chat.id, "Mounting failed. Please check your credentials.")

# Command handler for /trans command
@app.on_message(filters.command("trans"))
def trans_command(client, message):
    # Check if Google Drive is mounted
    if not drive.is_mounted():
        client.send_message(message.chat.id, "Google Drive is not mounted. Please use /mount to mount Google Drive.")
        return

    # Extract the link from the command
    command_parts = message.text.split()
    if len(command_parts) < 2:
        client.send_message(message.chat.id, "Invalid command format. Please use /trans <link>.")
        return

    link = command_parts[1]

    # Check the size of the link
    size = get_link_size(link)

    if size > 5:  # Size limit in GB
        client.send_message(message.chat.id, "The link size exceeds 5GB. Transfer is not allowed.")
        return

    # Start the transfer process
    client.send_message(message.chat.id, "Starting transfer process...")
    transfer_files(link)

# Function to get the size of a file or folder given its link
def get_link_size(link):
    # Code to get the size of the link (you can implement this based on your requirements)
    # Return the size in GB
    return 0

# Function to transfer files from Mega to Google Drive
def transfer_files(link):
    # Code to transfer files from Mega to Google Drive (you can implement this based on your requirements)
    pass

# Command handler for /stop command
@app.on_message(filters.command("stop"))
def stop_command(client, message):
    # Check if Google Drive is mounted
    if drive.is_mounted():
        # Unmount Google Drive
        command = "google-drive-ocamlfuse -label my_drive -cc"
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Send a success message
        client.send_message(message.chat.id, "Google Drive unmounted successfully.")
    else:
        client.send_message(message.chat.id, "Google Drive is not mounted.")

# Run the bot
app.run()
