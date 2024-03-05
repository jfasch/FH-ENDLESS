Generating A Sine Wave Pattern Over Time
========================================

The CAN controller mockup generates a sine wave onto its CAN
interface. This is how it's done.

Base Operation
--------------

.. jupyter-execute::

   from math import pi, sin

   def mysin(x, amplitude, hz, phase_shift, vertical_shift):
       return amplitude * sin(hz*(x+phase_shift)) + vertical_shift

   mysin(2*pi, hz=10, amplitude=5, phase_shift=pi/2, vertical_shift=37)

Fancy Plotting, And Heavy Dependencies 
--------------------------------------

.. jupyter-execute::

   import matplotlib.pyplot as plt
   import numpy

.. jupyter-execute::

   xaxis = numpy.linspace(0, 2*pi)
   xaxis

.. jupyter-execute::

   plt.plot(xaxis, [mysin(x, hz=10, amplitude=5, phase_shift=pi/2, vertical_shift=37) for x in xaxis])

