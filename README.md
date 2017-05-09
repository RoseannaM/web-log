# web-log
Basic multi-user blog created with Google app engine.
The live version of this project is here: **[Web-log](https://web-log-167111.appspot.com/)**
 
### How to run the project:
1. Install the Google App Engine 
2. Clone the repo to your device: [https://github.com/RoseannaM/web-log](../) 
3. Once installed, cd to the blog directory and install requirements with pip
4. Type the command ```dev_appserver.py ./``` in your terminal.
5. This will run the local dev server 
[Refer to the docs for troubleshooting](https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server)

### Inspect the code
Comments have been left in the file to explain most of the methods.

**Note**, the env.py file has been omitted from the repo. Please create another env.py file containing a ```get_secret()``` method. All it does is generate a string :) Or, for dev purposes, simply inclue the secret var in your blog.py file. 

<img src="https://web-log-167111.appspot.com/static/webblogicon.png" width="100">






