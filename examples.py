#!/usr/bin/python3

# This file is part of SunlightDPD - a home for open source software
# related to the dissipative particle dynamics (DPD) simulation
# method.

# Based on an original code copyright (c) 2007 Lucian Anton.
# Modifications copyright (c) 2008, 2009 Andrey Vlasov.  Additional
# modifications copyright (c) 2009-2016 Unilever UK Central Resources
# Ltd (Registered in England & Wales, Company No 29140; Registered
# Office: Unilever House, Blackfriars, London, EC4P 4BQ, UK).

# SunlightDPD is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# SunlightDPD is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with SunlightDPD.  If not, see <http://www.gnu.org/licenses/>.

# The examples here are described more fully in the documentation.

import matplotlib.pyplot as plt
from oz import wizard as w

# In these functions the final state is the same as the starting
# state, and the system is left in the solved condition.

# Function calculates the pressure by integrating the compressibility
# along an isotherm.

def cr_press(drho):
    p_xc = prev = 0.0
    n = int(w.rho[0]/drho + 0.5)
    w.cold_start = 1
    for i in range(n):
        w.rho[0] = drho * (i + 1.0)
        w.hnc_solve()
        p_xc = p_xc + 0.5*drho*(prev + w.comp_xc)
        prev = w.comp_xc
    return w.rho[0] + p_xc

# Function calculates the excess free energy per particle by coupling
# constant integration along an isochore.

def fnex1(dA):
    fnex_xc = prev = 0.0
    n = int(w.arep[0,0]/dA + 0.5)
    w.cold_start = 1
    for i in range(n):
        w.arep[0,0] = dA * (i + 1.0)
        w.dpd_potential(1)
        w.hnc_solve()
        curr = w.un_xc / w.arep[0,0]
        fnex_xc = fnex_xc + 0.5*dA*(prev + curr)
        prev = curr
    return w.un_mf + fnex_xc

# Function calculates the excess free energy per particle by
# integrating the chemical potential along an isotherm.

def fnex2(drho):
    fvex = prev = 0.0
    n = int(w.rho[0]/drho + 0.5)
    w.cold_start = 1
    for i in range(n):
        w.rho[0] = drho * (i + 1.0)
        w.hnc_solve()
        fvex = fvex + 0.5*drho*(prev + w.muex[0])
        prev = w.muex[0]
    return fvex / w.rho[0]

w.initialise()
w.arep[0,0] = A = 25.0
w.dpd_potential(1)
w.rho[0] = rho = 3.0
w.hnc_solve()

print('\n*** Example 5.1 ***\n')
print('rho =', rho, ' A =', A)
print('pressure =', w.press)
print('energy density =', w.uv)

plt.figure(1)  # This will be g(r)
imax = int(3.0 / w.deltar)
plt.plot(w.r[0:imax], 1.0+w.hr[0:imax,0,0])
plt.xlabel('$r$')
plt.ylabel('$g(r)$')

plt.figure(2)  # This will be S(k)
jmax = int(25.0 / w.deltak)
plt.plot(w.k[0:jmax], w.sk[0:jmax,0,0]/rho)
plt.xlabel('$k$')
plt.ylabel('$S(k)$')

plt.show()

print('\n*** Example 5.2 ***\n')
print('CR pressure =', cr_press(0.05))
print('VR pressure =', w.press)

print('\n*** Example 5.3 ***\n')
print('energy fnex =', fnex1(0.1))
print('mu fnex =    ', fnex2(0.05))
print('HNC fnex =   ', w.fnex)
