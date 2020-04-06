## Corona Statistics CLI

Get the latest coronavirus statistics directly from the CLI.

> Please make sure that you have `Python 3` up and running on your machine.

![Global](https://i.imgur.com/r7e21Th.png) 

![Denmark](https://i.imgur.com/Juex7sH.png)

```bash
git clone git@github.com:ahmadmayahi/coronavirus-cli.git
cd coronavirus-cli
pip3 install -r requirements.txt

# Get the statistics
python3 corona.py

# Statistics for a specific country (alpha2 code)
python3 corona dk # Denmark
python3 corona us # United States
python3 corona au # Australia

# Make the script available globally
sh install.sh
corona
```
