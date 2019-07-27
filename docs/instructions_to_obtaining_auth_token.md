# Getting an Auth Token

Guide: https://developer.spotify.com/documentation/general/guides/authorization-guide/

1. Create a spotify account and then log into the following and create a web app.  
https://developer.spotify.com/dashboard/

2. Note down your:  
i. Client ID  
ii. Client Secret  
iii. Redirect URI (edit settings): I just have `https://localhost:8888/callback/`

3. The redirect_uri needs to be "URL encoded" before you can use it. Just google for a URL encoder.

4. Open the following in the brower, using your client_id and encoded redirect_uri  
`https://accounts.spotify.com/authorize?client_id=...&response_type=code&redirect_uri=https%3A%2F%2Flocalhost%3A8888%2Fcallback%2F` 

5. Accept the access request pop up

6. You can grab the authorization code needed to request access token from the URL in the redirct_uri that you should get taken to.  
It's the part after the code=  
e.g the URL was `https://localhost:8888/callback/?code=AQAG6uFr2Mka4...`
		

7. Run the following in the command line  
`curl -H "Authorization: Basic NjdlNTU4MTU4NWVjNDM3ZDhjNDVlMDkyYTU0YTQzOWU6NWU1M2RhMmU5MmNhNDgwYmE2M2I4M2Q4ZjY4OGExZTM=" -d grant_type=authorization_code -d code=AQAG6uFr2Mka4IQtFgtUDgKp5EOClsGd9kieHbjSRPiM95AMqten7oWApO5u6r8ubOjy-c5u77HUZ7uOFCtm-vzahv5xCuXdZjpVbzUn66Iloni8pRPmDQ7pkbZ6l3WvDH4AxQCOby3emhapD-xN-XYW1FpdKU6hl6eWDx5INCIdFLZ0VVtT0mlZERtiqmdLpoT2wifPQTs -d redirect_uri=https%3A%2F%2Flocalhost%3A8888%2Fcallback%2F https://accounts.spotify.com/api/token`  
Notes:  
i. The code after Basic is the **client_id:client_secret encoded in base 64**  
ii. The code after code= is the authorization code generated in the above steps  
iii. The redirect_uri is encoded again as before

8. Copy your Auth Token (access_token)