==========
Installing
==========

Mesa Configuration Tool

.. Note:: Tested on Debian 10, 11, 12, 13 and Linux Mint 20.2 but it should work on
	other Debian type OS's.

.. Note:: Requires Python 3.6 or newer to work.

Install with apt
----------------

The advantage of using apt to install the Mesa Configuration Tool GUI is when a
new version of MesaCT GUI is released apt will know a new version is avaliable
when you run `sudo apt update`. This will allow you to install the new version
of MesaCT GUI along with other Debian software.

The first command will ask for your password. Neither command will print
anything in the terminal.

For a PC to create an apt sources file for MesaCT GUI copy and paste this command
in a terminal
::

	echo 'deb [arch=amd64] https://gnipsel.com/mesact/apt-repo stable main' | sudo tee /etc/apt/sources.list.d/mesact.list

For a Raspberry Pi 64 bit create an apt sources file for MesaCT GUI copy and
paste this command in a terminal
::

	echo 'deb [arch=arm64] https://gnipsel.com/mesact/apt-repo stable main' | sudo tee /etc/apt/sources.list.d/mesact.list

For a Raspberry Pi 32 bit create an apt sources file for MesaCT GUI copy and
paste this command in a terminal
::

	echo 'deb [arch=armhf] https://gnipsel.com/mesact/apt-repo stable main' | sudo tee /etc/apt/sources.list.d/mesact.list

To check the above command worked you can list the file with this command
::

	ls /etc/apt/sources.list.d

.. image:: /images/install-01.png
   :align: center


Next get the public key for MesaCT GUI and copy it to trusted.gpg.d
::

	sudo curl --silent --show-error https://gnipsel.com/mesact/apt-repo/pgp-key.public -o /etc/apt/trusted.gpg.d/mesact.asc

If curl is not installed you can install it with the following command
::

	sudo apt install curl

Next update apt
::

	sudo apt update

If you have MesaCT GUI installed you can see what packages can be upgraded with
the following command
::

	apt list --upgradable

If MesaCT GUI is not installed you can install it with the following command
::

	sudo apt install mesact

Manual Install
--------------

If you don't have an internet connection you can install the Mesa Configuration
Tool using the deb file. Download and copy the .deb file to your computer.

Latest Version of the Mesa Configuration Tool is in the
`Releases <https://github.com/jethornton/mesact/releases>`_

Select the one that suits your OS and download.

Open the File Manager and right click on the file and open with Gdebi then install.

.. Warning:: The graphical Gdebi does not work on the LinuxCNC chosen desktop so
   you have to use the terminal to install a deb file.

If you don't have Gdebi installed you can install it from a terminal
::

	sudo apt install gdebi

If the graphical version of gdebi has problems you can run it from a
terminal in the directory where you downloaded the deb with n.n.n replaced
by the version your installing.
::

	sudo gdebi mesact_n.n.n_amd64.deb

If you don't have LinuxCNC installed then the mesact Configuration tool
will show up in the Applications > Other menu otherwise it will be in
the CNC menu.

If you have problems try running from a terminal with:
::

	mesact

To flash firmware to the mesact you need to install 
`mesaflash <https://github.com/LinuxCNC/mesaflash>`_ from the LinuxCNC
repository.

To uninstall the mesact Configuration Tool right click on the .deb file
and open with Gdebi and select `Remove Package`.

To check for newer versions Help > Check for Updates

To upgrade the mesact Configuration Tool delete the .deb file and download
a fresh copy then right click on the .deb file and open with Gdebi and
select `Reinstall Package`

