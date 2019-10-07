from math import e
#use temp in Kelvin
def latent_heat(temp):
	"""L_v"""
	C = 4187
	C_pv = 1870
	T_0 = 273
	L_v = 2.5*10**6 - (C - C_pv) * (temp - T_0)
	return L_v
def pressure_vapor(temp):
	"""e_vs in Pa"""
	L_v = latent_heat(temp)
	R_v = 461.5
	T_0 = 273
	e_v = 611 * (e ** (L_v / R_v * (1 / T_0 - 1 / temp)))
	return e_v # Pa
def content_vapor(e_v, temp, pressure):
	"""q_vs in g / kg"""
	q_vs = 0.622 * pressure_vapor(temp) / pressure /100
	return q_vs
def potential_temp_e(temp, pressure, q_v):
	"""theta_e, 
	if the air parcel is saturared, use 9999 in q_v."""
	R_d = 287
	C_p = 1005
	theta = temp * (1000 / pressure) ** (R_d / C_p)
	e_v = pressure_vapor(temp) / 100 #hPa
	if q_v == 9999:
		q_v = content_vapor(e_v, temp, pressure)
	else: 
		pass
	L_v = latent_heat(temp)
	theta_e = theta * e ** (L_v * q_v / C_p / temp)
	return theta_e

#A part
print("A CONDITION:")
temp_a = 32 + 273.
pressure_a = 1000.
t_d_a = 28 + 273.
e_v_a = pressure_vapor(t_d_a)

q_v_a = content_vapor(e_v_a, t_d_a, pressure_a)
print("qv_a:", q_v_a, "g / kg")
theta_e_a = potential_temp_e(temp_a, pressure_a, q_v_a)
print("theta_e in A: ", theta_e_a)
print("=================================")
#B part
print("B CONDITION:")
pressure_b = 750.
temp_b = 20 + 273.
e_vs_b = pressure_vapor(temp_b)
q_vs_b = content_vapor(e_vs_b, temp_b, pressure_b)
print("qv_b:", q_vs_b, "g / kg")
theta_e_b = potential_temp_e(temp_b, pressure_b, 9999)
print("theta_e in B: ", theta_e_b)


while True:
	if (theta_e_b - theta_e_a) > 1 :
		temp_b -= 1e-5
		theta_e_b = potential_temp_e(temp_b, pressure_b, 9999)
		#print("theta_e_b: %f" % theta_e_b)
	else:
		print("\n==================")
		print("Temperature_b %f" % (temp_b - 273))
		break

######2.#######
e_vs_b = pressure_vapor(temp_b)
print("e_vs_b:", e_vs_b/100, "hPa")
q_vs_b = content_vapor(e_vs_b, temp_b, 750)
print("q_vs_b:", q_vs_b, "g / kg")
