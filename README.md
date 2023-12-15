<h1>User Data Command-line Interface</h1>

This Command-line Interface (CLI) provides functionality to perform various actions on user data.

<h2>Setup</h2>

1. Clone the repository:
```bash
git clone https://github.com/ZbigniewKorycki/recruitement-task-backend-internship
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
````

<h2>Usage</h2>

Run the CLI by executing cli.py and pass a command along with user login and password.

<h3>Available Commands:</h3>
<ul>
<li><b>print-all-accounts:</b> Print number of all user accounts.</li>
<li><b>print-oldest-account:</b> Print information about the oldest user account.</li>
<li><b>group-by-age:</b> Group children by age.</li>
<li><b>print-children:</b> Print children of a user.</li>
<li><b>find-similar-children-by-age:</b> Find users with children of similar ages.</li>
<li><b>create-database:</b> Create a user database.</li>
</ul>

<h3>Command Syntax:</h3>

```bash
python cli.py <command> --login <user_login> --password <user_password>
```

<h3>Example:</h3>

```bash
python cli.py print-all-accounts --login briancollins@example.net --password R9AjA5nb$!
```

<h2>Additional Information</h2>

This CLI project comes with built-in sample user data available in structured formats such as JSON, XML, and CSV. To use different data, follow these steps:

1. <b>Manual Data Upload:</b> If you want to use different user data, manually upload your data files (in JSON, XML, or CSV format) to the project directory.

2. <b>Modify Data Path:</b> Change the data paths in the <b>'users_data_processor.py'</b> file under the <b>'paths'</b> variable. Update the paths to point to your uploaded data files.

<h2>Authors</h2>
<ul>
  <li> <a href="https://github.com/ZbigniewKorycki">Zbigniew Korycki GitHub Profile</a></li>
</ul>

<h2>License</h2>
<ul>
  <li> This project is licensed under the MIT License - see the <a href="https://choosealicense.com/licenses/mit/">LICENSE file</a> for details.</li>
</ul>
