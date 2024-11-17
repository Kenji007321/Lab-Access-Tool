Date created: 2024/11/4
Current version: Ver 1.0

Author: Kenji Nakajima

<Description>
This GUI tool is for nework administration work in lab/datacenter.
It mainly serves as an access information management tool for your backbone switches
and access control switches.
This is especially usefull for lab environments that do not have the telnet protocol
allowed for security reasons, or ssh access is not set up on all devices.

The libraries/modules used for this project:
- pandas
- tkinter
- subprocess
- os

<Manual>
The GUI consists of 3 menus. 'Main menu', 'Add/Update menu' and 'Delete menu'.
The 'Main menu' is for connecting to your network devices.
The 'Add/Update menu' is for adding new access information or overwriting the old ones.
The 'Delete menu' is to delete any access information from the list.

You can work with two files, 'Backbone' file and 'Access Server' file.
The 'Backbone' file uses telnet and opens Tera Term, while the 'Access Server' file uses both telnet and ssh and opens Putty

The 'Name' data will display your devices depending on what 'Rack' is selected from the pulldown menu.

<Conditions>
Conditions for adding new access information are as follows:
1. 'Host' and 'Port' entry must not include any spaces
2. The first and last character in the 'Name' entry must not be a space
3. 'Host' and 'Name' entry must not be more than 20 characters
4. 'Host' and 'Port' entry must not contain full-width characters
5. 'Port' entry must be a number and not be more than 4 digits
6. Must not have duplicate 'Names' in the same file

*The file path for the Backbone and Access Server files must be changed to the correct path.