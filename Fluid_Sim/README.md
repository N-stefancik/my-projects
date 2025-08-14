Video Example for the Fluid Simulation

https://github.com/user-attachments/assets/2bac1ca1-03c1-4130-a4b5-15d0da099ac1

Interactive Fluid Simulation
A real-time 2D fluid simulation using Smoothed Particle Hydrodynamics (SPH) with interactive mouse controls and high-performance visualization. Built with Python, NumPy, VisPy, and accelerated with Numba JIT compilation.
Overview
This project implements a physically-based fluid simulation that demonstrates realistic fluid behavior including:

Particle-based fluid dynamics using SPH method
Real-time density calculations and pressure forces
Viscosity effects for realistic fluid flow
Interactive mouse-based fluid manipulation
Boundary collision handling with damping
Color-coded visualization based on particle velocity

Features
Core Simulation

SPH Algorithm: Smoothed Particle Hydrodynamics for realistic fluid behavior
Real-time Performance: Optimized with Numba JIT compilation for 60+ FPS
Density-based Forces: Pressure gradients drive particle movement
Viscosity Modeling: Realistic fluid friction and smoothing
Boundary Physics: Collision detection with energy dissipation

Interactive Controls

Mouse Drag: Click and drag to apply forces to nearby particles
Dynamic Forces: Real-time force application based on mouse movement
Adjustable Influence: Configurable drag radius and force strength
Velocity Visualization: Color-coded particles showing speed (plasma colormap)

Visualization

Real-time Rendering: Smooth 60 FPS visualization using VisPy
Particle System: 500 interactive fluid particles
Boundary Visualization: Fixed boundary particles for containment
Speed Mapping: Dynamic color coding from slow (purple) to fast (yellow)

Requirements
python >= 3.7
numpy
vispy
matplotlib
numba
Installation
bashpip install numpy vispy matplotlib numba
Usage
Running the Simulation
bashpython fluid_simulation.py
Controls

Left Mouse Button: Click and drag to apply forces to fluid
Mouse Movement: Drag velocity affects particle acceleration
Pan/Zoom: Use VisPy camera controls to navigate the view

Simulation Parameters
Key parameters that can be modified in the code:
pythonN = 100                    # Grid size (100x100)
num_particles = 500        # Number of fluid particles
smoothing_radius = 15      # SPH kernel radius
dt = 0.003                # Time step (smaller = more stable)
damping_factor = 0.5      # Boundary collision damping
viscosity_coefficient = 3  # Fluid viscosity strength
Algorithm Details
Smoothed Particle Hydrodynamics (SPH)
SPH is a computational method for simulating fluid dynamics by representing the fluid as a collection of particles.
Key Components:
1. Smoothing Kernel
pythonW(r,h) = (6/(π·h⁴)) · (h-r)² for r < h, 0 otherwise

Defines particle influence radius
Ensures smooth force transitions
Provides mathematical foundation for SPH

2. Density Calculation
pythonρᵢ = Σⱼ mⱼ · W(|rᵢ - rⱼ|, h)

Each particle's density based on nearby neighbors
Includes boundary particle contributions
Forms basis for pressure calculations

3. Pressure Forces
pythonFᵢ = -∇p = -Σⱼ mⱼ · (pᵢ + pⱼ)/(2ρⱼ) · ∇W(|rᵢ - rⱼ|, h)

Particles repel when density is high
Creates realistic fluid spreading behavior
Implements pressure gradient forces

4. Viscosity Forces
pythonFᵥᵢₛ = μ · Σⱼ mⱼ · (vⱼ - vᵢ)/ρⱼ · ∇²W(|rᵢ - rⱼ|, h)

Smooths velocity differences between particles
Provides realistic fluid friction
Stabilizes the simulation

Code Structure
Core Classes and Functions
Simulation Core

smoothing_kernel(): SPH smoothing kernel function
smoothing_kernel_derivative(): Kernel gradient for force calculations
calculate_density(): Computes particle density using SPH
calculate_gradient(): Computes pressure and interactive forces
calculate_viscosity(): Handles viscous forces between particles

Optimization

@jit(nopython=True): Numba compilation for performance
@jit(parallel=True): Parallel processing for density updates
Vectorized Operations: NumPy array operations for efficiency

Visualization

VisPy Scene: Hardware-accelerated rendering
Real-time Updates: 60 FPS particle position and color updates
Interactive Camera: Pan/zoom capabilities

Mouse Interaction

on_mouse_press(): Initiates interactive forces
on_mouse_move(): Updates drag position and velocity
on_mouse_release(): Deactivates interactive forces

Performance Optimizations
Numba JIT Compilation

All computational kernels compiled to machine code
10-100x speedup over pure Python
Parallel processing for density calculations

Memory Efficiency

Pre-allocated NumPy arrays
In-place operations where possible
Efficient boundary particle management

Algorithmic Optimizations

Vectorized distance calculations
Efficient neighbor searching
Optimized force accumulation

Physical Accuracy
The simulation implements several physically-based features:
Fluid Properties

Mass Conservation: Particle count remains constant
Momentum Conservation: Newton's laws applied to particle interactions
Realistic Viscosity: Velocity smoothing between neighboring particles

Boundary Conditions

Collision Response: Particles bounce off boundaries with damping
Energy Dissipation: Realistic energy loss during collisions
Containment: Fluid remains within simulation bounds

Interactive Forces

Distance-based Influence: Force strength decreases with distance
Velocity Coupling: Mouse movement velocity affects particles
Realistic Response: Particles follow mouse with natural lag

Applications and Extensions
Educational Use

Demonstrates fluid mechanics principles
Visualizes SPH algorithm in action
Interactive physics exploration

Potential Extensions

3D Simulation: Extend to three dimensions
Multiple Fluids: Different particle types and properties
Temperature Effects: Heat transfer and thermal dynamics
Surface Tension: Implement cohesive forces
Obstacles: Add interactive solid objects
Particle Sources/Sinks: Dynamic particle creation/destruction

Performance Scaling

GPU Acceleration: CUDA or OpenCL implementation
Spatial Hashing: Efficient neighbor finding for larger systems
Adaptive Time Stepping: Dynamic dt based on simulation stability

