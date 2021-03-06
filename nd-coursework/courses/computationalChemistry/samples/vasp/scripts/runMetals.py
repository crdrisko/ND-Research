#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Name: runMetals.py - Version 1.0.0
# Author: Cody R. Drisko (crdrisko)
# Date: 11/21/2019-11:44:17
# Description:


### Packages ###
import numpy as np
import matplotlib.pyplot as plt
from sys import argv

## ASE ##
from ase import Atoms, Atom
from ase.io import write
from ase.visualize import view
from ase.eos import EquationOfState
from ase.build import bulk
from ase.build.surface import fcc111, add_adsorbate
from ase.dft.dos import DOS

## VASP ##
from vasp import *
from vasp.vasprc import VASPRC

VASPRC['queue.q'] = 'long'
VASPRC['queue.nprocs'] = 24
VASPRC['queue.pe'] = 'mpi-24'


### Calculations ###
for metal in ['Cu', 'Ag', 'Au']:
	if argv[1] == "Q1":
		## Question 1 - Single Metal Atoms ##
		metal_atom = Atoms( [ Atom(metal, [0, 0, 0]) ],
              	 	 	cell=(8, 9, 10) )
		metal_atom.center()

		calc = Vasp('%s/%s-atom' %(metal, metal),
            	xc = 'PBE',    	## the exchange-correlation functional
        	ismear = 1,        	## Methfessel-Paxton smearing
         	 encut = 400,		## energy cutoff
         	 atoms = metal_atom)

		calc.calculate()

	elif argv[1] == "Q2":
		## Question 2 - k-point convergence ##
		kPoints = [3, 5, 7, 9, 11]

		for k in kPoints:
			metal_cubic = bulk(metal, 'fcc', cubic = True)

			calc = Vasp('%s/%s-kpt-convergence/kpt-%s' %(metal, metal, k),
					xc = 'PBE',
				ismear = 1,
				 encut = 400,
				  kpts = [k,k,k],
				 atoms = metal_cubic)

			calc.calculate()

	elif argv[1] == "Q3":
		## Question 3 - Finding bulk metal lattice constants ##
		if metal == 'Cu':
			exp = 3.61
		elif metal == 'Ag':
			exp = 4.09
		elif metal == 'Au':
			exp = 4.08

		A = np.linspace(exp * 0.9, exp * 1.1, 7)

		for a in A:
			metal_cubic = bulk(metal, 'fcc', a = a, cubic = True)

			calc = Vasp('%s/%s-EOS/a-%1.2f' %(metal, metal, a),
					xc = 'PBE',
				ismear = 1,
				 encut = 400,
				  kpts = [9,9,9],		## Converged k-points from Q2
				 atoms = metal_cubic)

			calc.calculate()
	
	elif argv[1] == "Q5":
		## Question 5 - Surfaces and Surface Energies ##
		if metal == 'Cu':
			a = 3.636
		elif metal == 'Ag':
			a = 4.147
		elif metal == 'Au':
			a = 4.158
		
		atoms = fcc111(metal, size=(2,2,3), vacuum=10.0, a=a)

		calc = Vasp('%s/%s-surface' %(metal, metal),
				xc = 'PBE',
			ismear = 1,
			 encut = 400,
			ibrion = 2,
			  kpts = [9,9,1],
			   nsw = 20,
			 atoms = atoms)

		calc.calculate()
	
	elif argv[1] == "Q6":
		## Question 6 - Adsorbates and Adsorption Energies ##
		if metal == 'Cu':
			a = 3.636
		elif metal == 'Ag':
			a = 4.147
		elif metal == 'Au':
			a = 4.158

		atoms = fcc111(metal, size=(2,2,3), vacuum=10.0, a=a)
		add_adsorbate(atoms, 'O', height=1.2, position='fcc')

		calc = Vasp('%s/O-on-%s-fcc' %(metal, metal),
				xc = 'PBE',
			ismear = 1,
			 encut = 400,
			ibrion = 2,
			  kpts = [9,9,1],
			   nsw = 20,
			 atoms = atoms)

		calc.calculate()

	elif argv[1] == "Q7":
		## Question 7 - Density of States ##

		# Metal Surface #
		calc = Vasp('%s/%s-surface' %(metal, metal))
		atoms = calc.get_atoms()

		calc = Vasp('%s/%s-ados' %(metal, metal),
				xc = 'PBE',
			ismear = 1,
			 encut = 400,
			  kpts = [9,9,1],
			lorbit = 10,
			 atoms = atoms)

		calc.calculate()

		# Adsorbate #
		calc = Vasp('%s/O-on-%s-fcc' %(metal, metal))
		atoms = calc.get_atoms()

		calc = Vasp('%s/O-on-%s-fcc-ados' %(metal, metal),
				xc = 'PBE',
			ismear = 1,
			 encut = 400,
			  kpts = [9,9,1],
			lorbit = 10,
			 atoms = atoms)

		calc.calculate()


### Plotting ###
if argv[1] == "Plot2":
	data_Cu = np.loadtxt("Cu/energies.dat", dtype=float)
	N_Cu= np.size(data_Cu)
	kpoints_Cu = data_Cu[0:N_Cu:1, 0]
	energies_Cu = data_Cu[0:N_Cu:1, 1]

	data_Ag = np.loadtxt("Ag/energies.dat", dtype=float)
	N_Ag = np.size(data_Ag)
	kpoints_Ag = data_Ag[0:N_Ag:1, 0]
	energies_Ag = data_Ag[0:N_Ag:1, 1]

	data_Au = np.loadtxt("Au/energies.dat", dtype=float)
	N_Au = np.size(data_Au)
	kpoints_Au = data_Au[0:N_Au:1, 0]
	energies_Au = data_Au[0:N_Au:1, 1]

	plt.plot(kpoints_Cu, energies_Cu, 'ro-', label="Cu Metal")
	plt.plot(kpoints_Ag, energies_Ag, 'go-', label="Ag Metal")
	plt.plot(kpoints_Au, energies_Au, 'bo-', label="Au Metal")
	plt.xlabel("k-Points")
	plt.ylabel("Total Energy (eV)")
	plt.ylim(-15.5, -9.5)
	plt.legend()
	plt.savefig('images/metal-kpt-convergence.png')
	plt.show()

elif argv[1] == "Plot3":
	for metal in ['Cu', 'Ag', 'Au']:
		data = np.loadtxt("%s/%s-EOS/energies.dat" %(metal, metal), dtype=float)

		N = np.size(data)
		lattice = data[0:N:1, 0]
		energies = data[0:N:1, 1]
		volumes = data[0:N:1, 2]
			
		plt.plot(lattice, energies, 'bo-')
		plt.xlabel('Lattice constant ($\\AA$)')
		plt.ylabel('Total energy (eV)')
		plt.savefig('images/%s-fcc-lattice.png' %metal)
		plt.show()
	
		# Let's fit this to an equation of state

		eos = EquationOfState(volumes, energies, eos='birchmurnaghan')
		v0, e0, b = eos.fit()
		a0 = v0**(1/3)
		eos.plot(filename='images/%s-EOS.png' %metal, show = True)

		print(metal)
		print('Minimum Energy = {0:1.3f} eV'.format(e0))
		print('Optimal Volume = {0:1.3f} cubic angstroms'.format(v0))
		print('Optimal lattice constant = {0:1.3f} angstroms'.format(a0))
		print()

elif argv[1] == "Plot7":
	for metal in ['Cu', 'Ag', 'Au']:
		calc = Vasp('%s/O-on-%s-fcc-ados' %(metal, metal))

		p_energies, p_dos = calc.get_ados(12, 'p')
		plt.plot(p_energies, p_dos, label='O$_p$', lw=2)

		calc = Vasp('%s/%s-ados' %(metal, metal))
		clean_energies, d_dos = calc.get_ados(11, 'd')
		plt.plot(clean_energies, d_dos, label='%s$_d$' %metal, lw=2)

		plt.axvline(ls='-.', color='k', lw=2)
		plt.xlabel('Energy (eV)')
		plt.ylabel('DOS (arb. units)')
		plt.legend()
		plt.savefig('images/%s-adsorbate-dos.png' %metal)
		plt.show()
