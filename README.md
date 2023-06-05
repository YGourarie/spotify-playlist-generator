Song Extraction and Playlist Generation
This project is a script that extracts Spotify song links from a given text and creates a playlist using the Spotify API. The script requires your Spotify app credentials and a text file containing the desired input text.
I found it great to use an exported whatsapp chat to get all the songs that were sent!

Prerequisites
Before running the script, make sure you have completed the following steps:

Create a Spotify app on the Spotify Developer Dashboard (https://developer.spotify.com/dashboard/applications).
Obtain your Spotify app credentials (Client ID and Client Secret).
Create a .env file in the project directory and add the following lines, replacing YOUR_CLIENT_ID and YOUR_CLIENT_SECRET with your actual credentials:
makefile
Copy code
SPOTIFY_CLIENT_ID=YOUR_CLIENT_ID
SPOTIFY_CLIENT_SECRET=YOUR_CLIENT_SECRET
Install the necessary Python dependencies. You can do this by running the command pip install -r requirements.txt. Make sure you have Python and pip installed on your system before proceeding.
Usage
To use the script, follow these steps:

Provide the input text file: Replace the example text file (example.txt) in the project directory with your own text file. You can use any text source, such as an exported WhatsApp chat or a generated text file. Make sure to maintain the same file format and update the filename in the main function in script.py to reflect your new file name.

Customize the script (optional): If you want to change the playlist name, open script.py and modify the playlist_name variable under the main function.

Run the script: Execute the command python script.py in your command line or terminal to extract Spotify song links from the text file and generate a playlist.

Check the output: The script will print the extracted song links and create a new playlist with the specified name in your Spotify account.

Please note that the script requires a stable internet connection and valid Spotify app credentials in order to access the Spotify API.
