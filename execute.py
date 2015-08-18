from chinookPM import chinook_pm
from bellPM import bell_pm, bell_campus_pm
from acornPM import acorn_pm
from premierPM import premier_pm
from principlePM import principle_pm
from northwoodsPM import northwoods_pm
from emeraldPM import emerald_pm
from pioneerPM import pioneer_pm
from jenningsgroupPM import jennings_group_pm
from metcoPM import metco_pm
from fullhousePM import full_house_pm
from trioPM import trio_pm
from mallardPM import mallard_pm
from preferrednwPM import preferred_nw_pm
from umbrellaPM import umbrella_pm
from campusconnectionPM import campusconnection_pm
from valleyinvestmentPM import valleyinvestment_pm

from datetime import datetime
from threading import Timer

def update():
	acorn_pm()
	bell_pm()
	bell_campus_pm()
	campusconnection_pm()
	chinook_pm()
	emerald_pm()
	full_house_pm()
	jennings_group_pm()
	mallard_pm()
	metco_pm()
	northwoods_pm()
	pioneer_pm()
	preferred_nw_pm()
	premier_pm()
	principle_pm()
	trio_pm()
	umbrella_pm()
	valleyinvestment_pm()

now = datetime.today()
change = now.replace(day=now.day+1, hour=1, minute=0, second=0, microsecond=0)
difference = change - now
seconds = difference.seconds+1

t = Timer(seconds, update)
t.start()
