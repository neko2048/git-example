import matplotlib.pyplot as plt 

### parameter ###
dt = 0.1
time_length = 1000 # s
R1s = []
Z1s = []
V1s = []
R2s = []
Z2s = []
V2s = []
class Cloud_Drop:

	def __init__(self, radius, height, cloud_v):
		self.height = height # m
		self.cloud_v = cloud_v # m/s
		self.radius = radius # m
		self.velocity = cloud_v - 8000 * radius # m/s

	def moving(self):
		self.height += self.velocity * dt # m
		self.velocity = self.cloud_v - 8000 * self.radius # m/s

	def grow(self):
		dR = 5e-3 * self.radius # m/s
		self.radius += dR * dt

cloud_drop_1 = Cloud_Drop(radius = 5e-5, height = 250, cloud_v = 5)
cloud_drop_2 = Cloud_Drop(radius = 1e-4, height = 250, cloud_v = 5)
for i in range(int(time_length / dt)):
	cloud_drop_1.moving()
	cloud_drop_1.grow()
	cloud_drop_2.moving()
	cloud_drop_2.grow()
	R1s.append(cloud_drop_1.radius)
	Z1s.append(cloud_drop_1.height)
	V1s.append(cloud_drop_1.velocity)
	R2s.append(cloud_drop_2.radius)
	Z2s.append(cloud_drop_2.height)
	V2s.append(cloud_drop_2.velocity)
print("Completed")
print("SIZE_1:"+ str(R1s[-1] * 1e6))
print("SIZE_2:"+ str(R2s[-1] * 1e6))
#ZT graph
#plt.plot([x/10 for x in range(len(Z1s))], Z1s, label = 'Radius : 50 μm')
#plt.plot([x/10 for x in range(len(Z1s))], Z2s, label = 'Radius : 100 μm')
#plt.ylim(bottom = 0)
#plt.title("Height with Time")
#plt.xlabel('Time (s)')
#plt.ylabel('Height (m)')
#plt.legend()
#plt.show()
# ===
#RZ graph
#plt.plot(R1s, Z1s, label = 'Radius : 50 μm')
#plt.plot(R2s, Z2s, label = 'Radius : 100 μm')
#plt.ylim(bottom = 0)
#plt.title("Radius with Height")
#plt.xlabel('Radius (m)')
#plt.ylabel('Height (m)')
#plt.legend()
#plt.show()
plt.plot(R1s, label = 'radius = 5e-5')
plt.plot(R2s, label = 'radius = 1e-4')
plt.legend()
plt.show()