#!/usr/bin/env python

## 
 # ###################################################################
 #  PFM - Python-based phase field solver
 # 
 #  FILE: "input.py"
 #                                    created: 11/17/03 {10:29:10 AM} 
 #                                last update: 12/9/03 {2:25:25 PM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-17 JEG 1.0 original
 # ###################################################################
 ##

"""Diffusion equation input file

    Build a mesh, variable, and diffusion equation with fixed (zero) flux
    boundary conditions at the top and bottom and fixed value boundary
    conditions at the left and right.
    
    Iterates a solution and plots the result with gist.
    
    Iteration is profiled for performance.
"""

from meshes.grid2D import Grid2D
from phaseEquation import PhaseEquation
from solvers.linearPCGSolver import LinearPCGSolver
from boundaryConditions.fixedValue import FixedValue
from boundaryConditions.fixedFlux import FixedFlux
from iterators.iterator import Iterator
from viewers.grid2DGistViewer import Grid2DGistViewer
from variables.cellVariable import CellVariable
from phase.modularVariable import ModularVariable
from profiler.profiler import Profiler
from profiler.profiler import calibrate_profiler
import Numeric

phaseParameters={
    'tau' :        0.1,
    'epsilon' :    0.008,
    's' :          0.01,
    'alpha' :      0.015,
    'c2':          0.0,
    'anisotropy':  0.,
    'symmetry':    4.
    }

interiorValue = Numeric.pi
exteriorValue = Numeric.pi / 2.

L = 1.5
nx = 100
ny = 100
dx = L / nx
dy = L / ny

mesh = Grid2D(dx,dy,nx,ny)

phase = CellVariable(
    name = 'PhaseField',
    mesh = mesh,
    value = exteriorValue,
    viewer = Grid2DGistViewer
    )

theta = ModularVariable(
    name = 'Theta',
    mesh = mesh,
    value = Numeric.pi,
    viewer = Grid2DGistViewer,
    hasOld = 0
    )

phaseParameters['phi'] = phase
phaseParameters['theta'] = theta
phaseParameters['temperature'] = 1.


def func(x,L=L):
    r = L / 4.
    c = (L / 2., L / 2.)
    if (x[0] - c[0])**2 + (x[1] - c[1])**2 < r**2:
        return 1
    else:
        return 0

interiorCells = mesh.getCells(func)

theta.setValue(interiorValue,interiorCells)

eq = PhaseEquation(
    phase,
    solver = LinearPCGSolver(
	tolerance = 1.e-15, 
	steps = 1000
    ),
    boundaryConditions=(
    FixedValue(mesh.getExteriorFaces(), exteriorValue),
    ),
    parameters = phaseParameters
    )

it = Iterator((eq,))

# fudge = calibrate_profiler(10000)
# profile = Profiler('profile', fudge=fudge)
it.iterate(100,0.02)
# profile.stop()

phase.plot()

raw_input()

