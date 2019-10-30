import numpy as np
from numpy import linalg as LA

'''
Defines update functions for particles
'''

# Constants
K = 9.81


def zero_update_function(particle, thrust, step_length, thrust_velocity, thrust_degree):
    state = list(particle.state_list[-1])
    state[0] += step_length
    return tuple(state)


def gravitaional_pull_from_list(particle_list):
    def update_function(particle, thrust, step_length,thrust_velocity, thrust_degree):
        net_f = np.zeros((2, 1))
        time, position, velocity, fuel = particle.state_list[-1]

        for p in particle_list:
            if p.id != particle.id:
                distance_p = position - p.current_position()
                force_p = - ((K * particle.mass * p.mass)/(LA.norm(distance_p)
                                                           ** 2)) * (distance_p/LA.norm(distance_p))
                net_f += force_p

        # Add Thrust Logic Here #
        # I am assuming that thrust is in kilograms
        # Formula is dv = v_thrust log(mass initial/mass final)
        dv_thrust = thrust_velocity np.log(particle.state_list[-1][-1]/(particle.state_list[-1][-1] - thrust))
        dv_thrust = [dv_thrust np.cos(thrust_degree), dv_thrust np.sin(thrust_degree)]
        #########################
        net_a = net_f/particle.mass
        dv = dv_thrust + net_a * step_length
        avg_v = velocity + .5 * dv

        next_time = time + step_length
        next_position = position + avg_v * step_length
        next_velocity = velocity + dv
        next_fuel = fuel - thrust

        return (next_time, next_position, next_velocity, next_fuel)
    return update_function
