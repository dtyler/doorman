Cloud Doorman
=======
This project provides a basic configuration website for a cloud doorbell service created by my apartment-mate.

Serving
----------
Right now this is served behind nginx. It runs itself on port 5000.

Configuration
-----------------
Throughout the code there are references to 'configMap'. This is a dictionary populated by a YAML config file('config.yaml') which is assumed to live in the same directory as server.py. The keys which are expected to be in this file will be detailed here eventually. (Alternative just keep starting the server and filling in missing keys as it explodes on you until you find them all!)
