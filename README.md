# Covid-19 Tracker Dashboard

![abc](images/dashboard-4.png)

----
## Motivation
Covid-19 was(is) an unprecedented pandemic that [stole the jobs of 114 million people] in 2020 and the [lives of another 2.8 million] as of 1st April 2021.


Relying on data gathered by Our World In Data ([OWID]), this project hopes to extract and visualize the global status of covid-19 in order to better understand its progression.
The [OWID Database] is updated everyday at roughly 08:30 UTC.

From the visualization above, we can see that Gibraltar and Israel leads the world in fully vaccinated residents, at 84.6% and 55.5% of their population respectively.
 </br>

Other visualizations track the no. of cases and deaths in each country due to Covid-19, as well as the no. of people fully vaccinated.

----

## Installation
### Environment
For the rest of this set-up, we will assume a ```Ubuntu 16 (Xenial Xerus)``` environment. You may follow this guide to [launch an EC2 instance on AWS with Ubuntu]. I'll be using Vagrant + VirtualBox.

### Set-up Vagrant box
```bash
vagrant up
vagrant ssh
```

### Apt install repositories
```bash
sudo apt update && sudo apt upgrade -y
```
- Git

### Software
- Elasticsearch
- Kibana
- Python
    - Core
    - Pip

    python3 -m pip install --user --upgrade pip

Run script once for initial load 
<br><br>

----

## Data Generation
### Git clone this repository to the home directory of your user directory
```bash
cd ~
git clone https://github.com/hideyukikanazawa/covid19-dashboard.git
```
### Using a Python venv
Install the python virtual environment package and create a new virtual environment **dashboard-venv**. Then pip install required python modules from requirements.txt into your **dashboard-venv** venv:
```bash
python3 -m pip install venv --user
python3 -m venv ~/dashboard-venv

~/dashboard-venv/bin/pip3 install -r requirements.txt
```


### Load your dashboard data
```bash
/home/$USER/dashboard-venv/bin/python3 /home/$USER/covid-data-cronjob.py > /home/$USER/covid-data-cronjob.log 2>&1
```
> It might take ~ a minute or two for the execution to complete

### Enable cronjob

Edit your user's crontab file ( stored in **/var/spool/cron/crontabs** directory on Ubuntu ):
```bash
crontab -e
```

Append the following lines to the end of your crontab:
>CRON_TZ=UTC<br>
>30 08 * * * /home/$USER/dashboard-venv/bin/python3 /home/$USER/covid-data-cronjob.py > /home/$USER/ > covid-data-cronjob.log 2>&1
>
##### Remember to change $USER to the name of your user
##### First line sets cron timezone to be UTC<br>
##### Second line runs the python cronjob everyday at 08:30 UTC
<br>

----

## Kibana Set-up
Access your Kibana end-point @ ```localhost:5601``` on your preferred browser

Follow the instructions here to [import kibana dashboards] with ```~/covid19-dashboard/export.ndjson```. You may also choose to create customized visualizations/dashboards.
<br><br>
With that, you have your very own covid-19 dashboard which tracks the global status of each country!

![](images/dashboard-1.png)
![](images/dashboard-2.png)
![](images/dashboard-3.png)
(Data above is accurate as of *1st April 2021*)


Kudos!

## References
[stole the jobs of 114 million people]: https://www.weforum.org/agenda/2021/02/covid-employment-global-job-loss/
[lives of another 2.8 million]: https://www.worldometers.info/coronavirus/coronavirus-death-toll/
[OWID]: https://ourworldindata.org/
[OWID Database]: https://github.com/owid/covid-19-data/tree/master/public/data

[launch an EC2 instance on AWS with Ubuntu]: https://mobisoftinfotech.com/resources/mguide/launch-aws-ec2-server-set-ubuntu-16-04/
[import kibana dashboards]: https://support.logz.io/hc/en-us/articles/210207225-How-can-I-export-import-Dashboards-Searches-and-Visualizations-from-my-own-Kibana-