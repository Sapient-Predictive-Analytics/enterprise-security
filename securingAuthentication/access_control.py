# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 17:27:56 2025

@author: tom
"""

from requests_oauthlib import OAuth2Session from oauthlib.oauth2
import MobileApplicationClient
import subprocess
import torch
import clip
from PIL import Image

# Replace these with the actual client ID and URI
client_id = 'YOUR_CLIENT_ID' redirect_uri = 'YOUR_REDIRECT_URI'
# This should match the one you set in the Google Console
# Define the scope of the application
scope = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile' ]
# Create a client instance
client = MobileApplicationClient(client_id)
# Create an OAuth2 session
oauth = OAuth2Session(
    client=client, scope=scope, redirect_uri=redirect_uri)
# Get the authorization URL
authorization_url, state = oauth.authorization_url(
    'https://accounts.google.com/o/oauth2/auth',
    access_type="offline", prompt="select_account")
print('Please go to {} and authorize 
    access.'.format(authorization_url))
# Get the authorization response from the callback URL
redirect_response = input('Paste the full redirect URL here: ')
 # Fetch the token
token = oauth.fetch_token(
    'https://accounts.google.com/o/oauth2/token',
    authorization_response=redirect_response,
    client_secret='YOUR_CLIENT_SECRET')
print('Authentication successful, here is the token: ', token)


def set_selinux_context(filepath, selinux_type):
    """ Set the SELinux context for a specific file. """
    try:
        command = f'semanage fcontext -a -t 
            {selinux_type}"{filepath}"'
        subprocess.run(command, check=True, shell=True)
        subprocess.run(f'restorecon -v {filepath}', check=True, 
            shell=True)
        print(f"SELinux context for {filepath} set to 
            {selinux_type}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set SELinux context 
            for {filepath}: {str(e)}")
def get_selinux_context(filepath):
    """ Get the SELinux context for a specific file. """
    try:
        result = subprocess.run(f'ls -Z {filepath}',
        check=True, shell=True, capture_output=True, text=True)
        print(f"SELinux context 
            for {filepath}: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to get SELinux context 
            for {filepath}: {str(e)}")
# Example Usage
file_path = '/path/to/your/file'
selinux_type = 'httpd_sys_content_t'
# Example type, change as needed
set_selinux_context(file_path, selinux_type)
get_selinux_context(file_path)

# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load and preprocess the images
image_path1 = "path_to_face_image1.jpg"
image_path2 = "path_to_face_image2.jpg"
image1 = preprocess(Image.open(image_path1)).unsqueeze(0).to(device)
image2 = preprocess(Image.open(image_path2)).unsqueeze(0).to(device)

# Generate image embeddings
with torch.no_grad():
    image_features1 = model.encode_image(image1)
    image_features2 = model.encode_image(image2)
# Normalize the embeddings
image_features1 /= image_features1.norm(dim=-1, keepdim=True)
image_features2 /= image_features2.norm(dim=-1, keepdim=True)

# Calculate cosine similarity
similarity = torch.cosine_similarity(image_features1, image_features2)
print(f"Similarity: {similarity.item()}")

# Define a threshold
threshold = 0.8  # Adjust this value based on your needs
if similarity.item() > threshold:
    print("The faces match!")
else:
    print("The faces do not match.")
    
