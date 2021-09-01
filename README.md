# Python_file_upload_API
Flask-based RESTFUL web service to upload files on the remote server with multiple files post requests.


Required web server configuration file *web. config* has been attached there.


*scriptProcessor* is the crucial path location for fastcgi to bridge between python and server.


*add key="WSGI_HANDLER" value="something.app"* is the name of the specific API.


*add key="PYTHONPATH" value="C:\inetpub\wwwroot\somesitename"* is the name of the site created by the server
