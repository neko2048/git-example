import numpy as np 
import matplotlib
from matplotlib.pyplot import * 
import matplotlib.cm as cm
#from model_task5_formula import *

maxt = 900
## base state vector 
theta = np.full(shape=(nz, ), fill_value=300.)
theta_v = theta.copy()
qb = np.zeros(nz, )
pb = np.zeros(nz, )
pib = np.zeros(nz, )
rhou = np.zeros(nz, )
rhow = np.zeros(nz, )

## prognostic array (past, now, future step)
thp, th, thm = np.zeros((nx, nz)), np.zeros((nx, nz)), np.zeros((nx, nz))
up, u, um = np.zeros((nx, nz)), np.zeros((nx, nz)), np.zeros((nx, nz))
wp, w, wm = np.zeros((nx, nz)), np.zeros((nx, nz)), np.zeros((nx, nz))
pip, pi, pim = np.zeros((nx, nz)), np.zeros((nx, nz)), np.zeros((nx, nz))


def set_theta():
	"""set initial theta in grids and in level average"""
	for i in range(1, nx-1):
		for k in range(1, nz-1):
			rad = np.sqrt((((k - .5) * dz - zcnt) / radz)**2 + (dx * (i - xmid + .25) / radx)**2)
			# .5 and .25 to adjust the center to (0, zcnt)
			if rad <= 1:
				th[i, k] = 0.5 * sigma * (np.cos(rad * np.pi) + 1 )
	## set boundary condition
	th[0, :] = th[nx-2, :] # colume boundary
	th[nx-1, :] = th[1, :] # colume boundary
	th[:, 0] = th[:, 1]
	th[:, nz-1] = th[:, nz-2]
	
	#for i in range(nz):
	#	if i == 0 or i == nz-1:
	#		theta[i] = 300
	#	else:
	#		theta[i] = 300 + np.mean(th[1:nx-1, i])

	#theta_v[1:nz-1] = (theta[0:nz-2] + theta[1:nz-1]) / 2
	#theta_v[0], theta_v[nz-1] = theta_v[1], theta_v[nz-2]


def set_pib():
	"""set nondimensional pressure in level avarage"""
	for i in range(1, nz-1):
		if i == 1:
			pib[i] = (P_srf / P_0) ** (R_d / C_p)
		else: 
			pib[i] = pib[i-1] - dz * 2 * (g / C_p / (theta[i] + theta[i-1]))
	pib[0] = pib[1]
	pib[nz-1] = pib[nz-2]

def set_rho():
	"""calculate rhou and rhow"""
	mask = slice(1, nz-1)
	rhou[mask] = P_0 * pib[mask] ** (C_v / R_d) / (R_d * theta[mask])
	rhou[0], rhou[nz-1] = rhou[1], rhou[nz-2] # outer boundary = boundary
	
	rhow[mask] = (rhou[0:nz-2] + rhou[1:nz-1]) / 2
	rhow[0], rhow[nz-1] = rhow[1], rhow[nz-2] # outer boundary = boundary

def set_pi():
	"""calculate nondimensional perturbation """
	for i in range(1, nx-1):
		for k in reversed(range(1, nz-1)):
			tup = th[i, k+1] / theta[k+1]**2
			tdn = th[i, k] / theta[k]**2
			pi[i, k] = pi[i, k+1] - 0.5 * g / C_p * (tup + tdn) * dz

def set_bc(var):
	var[:, 0] = var[:, 1]
	var[:, nz-1] = var[:, nz-2]
	var[0, :] = var[nx-2, :]
	var[nx-1, :] = var[1, :]



## set up initial perturbation and their boundary
set_theta();
set_pib();
set_rho();
set_pi();
set_bc(th)
set_bc(pi)
thp = th.copy()
pip = pi.copy()


def du(i, k):
	hori_adv = -0.25 / dx * ((u[i+1, k] + u[i, k])**2 - (u[i, k] + u[i-1, k])**2)
	
	verti_adv = -0.25 / (rhou[k] * dz) * (rhow[k+1] * (w[i, k+1] + w[i-1, k+1]) * (u[i, k+1] + u[i, k]) -
	 rhow[k] * (w[i, k] + w[i-1, k]) * (u[i, k] + u[i, k-1]))
	
	pgf = - C_p * theta_v[k] / dx * (pi[i, k] - pi[i-1, k])
	return hori_adv + verti_adv + pgf

def dw(i, k):
	hori_adv = -0.25 / dx * ((u[i+1, k] + u[i+1, k-1]) * (w[i+1, k] + w[i, k]) - (u[i, k] + u[i, k-1]) * (w[i, k] + w[i-1, k]))

	verti_adv = -0.25 / (rhow[k] * dz) * (rhou[k] * (w[i, k+1] + w[i, k]) ** 2 - rhou[k-1] * (w[i, k] + w[i, k-1]) ** 2)

	pgf = - C_p * 0.5 * (theta_v[k] + theta_v[k-1]) * (pi[i, k] - pi[i, k-1]) / dz

	bouyancy = g * 0.5 * (th[i, k] / theta[k] + th[i, k-1] / theta[k-1])

	return hori_adv + verti_adv + pgf + bouyancy

def dth(i, k):
	hori_adv = - 0.5 / (dx) * (u[i+1, k] * (th[i+1, k] + th[i, k]) - u[i, k] * (th[i, k] + th[i-1, k]))

	verti_adv = -0.5 / (rhou[k] * dz) * (rhow[k+1] * w[i, k+1] * (th[i, k+1] + th[i, k]) - rhow[k] * w[i, k] * (th[i, k] + th[i, k-1]))

	verti_adv_mean = -1 / (dz * rhou[k]) * (rhow[k+1] * w[i, k+1] * (theta[k+1] - theta[k]) + rhow[k] * w[i, k] * (theta[k] - theta[k-1]))

	return hori_adv + verti_adv + verti_adv_mean

def dpi(i, k):
	first = 1 / dx * rhou[k] * theta_v[k] * (u[i+1, k] - u[i, k])

	second = 0.5 / dz * (rhow[k+1] * w[i, k+1] * (theta_v[k+1] + theta_v[k]) - rhow[k] * w[i, k] * (theta_v[k] + theta_v[k-1]))

	return -cs**2 / (rhou[k] * C_p * theta_v[k] ** 2) * (first + second)

def ani(time, var):
	xvisind = slice(1, nx-1)
	zvisind = slice(1, nz-1)
	if time % (5 * dt) == 0 : 
		m = contour(x_cor, z_cor, 
			var[xvisind, zvisind].transpose(), cmap = cm.coolwarm, levels=20)
		title('time:'+str(time))
		colorbar(m)
		draw()
		pause(0.01)
		clf()




time_count = 0

while nowt <= maxt - dt:
	for i in range(1, nx-1):
		for k in range(1, nz-1):
			um[i, k] = up[i, k] + 2 * dt * du(i, k);
			wm[i, k] = wp[i, k] + 2 * dt * dw(i, k);
			thm[i, k] = thp[i, k] + 2 * dt * dth(i, k);
			pim[i, k] = pip[i, k] + 2 * dt * dpi(i, k);

	set_bc(um)
	set_bc(wm)
	set_bc(thm)
	set_bc(pim)

	up = u.copy()
	u = um.copy()
	wp = w.copy()
	w = wm.copy()

	thp = th.copy()
	th = thm.copy()
	pip = pi.copy()
	pi = pim.copy()
	
	ani(nowt, th)
	time_count += 1
	nowt = dt * time_count
