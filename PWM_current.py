#Function to calculate the current from t=0 to t=tf  
import numpy as np
import math as math
#Inputs: inductance, resistance, final time, frequency, duty cycle(from 0.0 to 1.0) [all floats]
def current_LR_PWM(L,R,tf,freq,duty):	#Returns the tuple with [t,i] where t is from 0 to tf.
	dt = 0.001*tf/freq
	V_m = 3.3
	N = int(tf/dt) + 1
	time = np.linspace(0,tf,N)
	i = np.zeros(N)
	v = np.zeros(N)
	T = 1.0/freq
	tau = L/R
	i0_h = 0.0	#current at start of high cycle
	i0_l = 0.0	#current at the start of low cycle

	for k in range(0,N):
		if math.fmod(k*dt,T) < (duty*T):
			t_k = math.fmod(k*dt,T)  
			i[k] = (V_m/R) + (i0_h - V_m/R)*np.exp(-t_k/tau)	
			v[k] = V_m
			i0_l = i[k]	#Every time sets low current.so it goes in second condition it sets i_l as the latest current from high cycle
		else:
			t_k = math.fmod(k*dt,T) - duty*T
			i[k] = i0_l*np.exp(-t_k/tau)
			v[k] = 0.0
			i0_h = i[k]	#similar logic as i0_l

	return time, i, v

#Test code
'''
import matplotlib.pyplot as plt

x = current_LR_PWM(1e-3,100,2,1000.0,1.0)


plt.plot(x[0][0:100],x[2][0:100])
plt.show()
plt.plot(x[0][0:100],x[1][0:100])
plt.show()
'''