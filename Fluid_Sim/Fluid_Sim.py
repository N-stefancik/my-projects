import numpy as np
import vispy.scene
from vispy.scene import visuals
import time
import matplotlib.pyplot as plt
from numba import jit, prange

# Simulation parameters
N = 100  # Grid size (N x N)
num_particles = 500  # Number of fluid particles

G = 20  # Grid for tracking

damping_factor = 0.5  # Damping factor for boundary collisions
smoothing_radius = 15  # Smoothing radius for kernel function
dt = 0.003  # Time step for simulation
bps = 20
velocity_damping = 1  # Damping factor for velocities
viscosity_coefficient = 3  # Added viscosity coefficient

# Initialize with NumPy arrays
positions = np.random.rand(num_particles, 2) * N
velocities = np.zeros_like(positions)
densities = np.zeros(num_particles)
predictedPositions = positions.copy()

# Add drag variables
drag_active = False
drag_start_pos = np.array([-1, -1])
drag_current_pos = np.array([-1, -1])
drag_velocity = np.array([0., 0.])

# Pre-compute boundary particles as NumPy array
boundary_indices = np.arange(bps)
boundary_particles = np.zeros((4 * bps, 2))
boundary_particles[:bps, 0] = boundary_indices * 100 / bps
boundary_particles[bps:2*bps, 0] = 100
boundary_particles[bps:2*bps, 1] = boundary_indices * 100 / bps
boundary_particles[2*bps:3*bps, 0] = 100 - boundary_indices * 100 / bps
boundary_particles[2*bps:3*bps, 1] = 100
boundary_particles[3*bps:, 1] = 100 - boundary_indices * 100 / bps

# Vectorized grid management using NumPy operations
grid_cells = np.zeros((G, G, num_particles), dtype=np.int32)
grid_counts = np.zeros((G, G), dtype=np.int32)

@jit(nopython=True)
def smoothing_kernel(radius, distance):
    if distance >= radius:
        return 0
    val = (np.pi * radius**4)/6
    return (((radius-distance)**2)/val)

@jit(nopython=True)
def smoothing_kernel_derivative(radius, distance):
    if distance > radius:
        return 0
    return 12*(distance-radius)/(np.pi*radius**4)

@jit(nopython=True)
def calculate_density(point_x, point_y, positions, boundary_particles, num_particles, bps):
    density = 0
    mass = 1
    
    # Vectorized distance calculation for normal particles
    for i in range(num_particles):
        distance = np.sqrt((positions[i, 0] - point_x)**2 + (positions[i, 1] - point_y)**2)
        density += mass * smoothing_kernel(smoothing_radius, distance)
    
    # Vectorized distance calculation for boundary particles
    for i in range(4 * bps):
        distance = np.sqrt((boundary_particles[i, 0] - point_x)**2 + 
                         (boundary_particles[i, 1] - point_y)**2)
        density += mass * smoothing_kernel(smoothing_radius, distance)
    
    return density + 0.001

@jit(nopython=True)
def calculate_viscosity(point_x, point_y, positions, velocities, num_particles):
    viscosity_force = np.zeros(2)
    
    for i in range(num_particles):
        diff = positions[i] - np.array([point_x, point_y])
        distance = np.sqrt(np.sum(diff**2))
        
        if 0 < distance < smoothing_radius:
            # Calculate velocity difference
            velocity_diff = velocities[i]
            weight = smoothing_kernel(smoothing_radius, distance)
            viscosity_force += velocity_diff * weight * viscosity_coefficient
            
    return viscosity_force

@jit(nopython=True, parallel=True)
def update_densities(positions, densities, boundary_particles, num_particles, bps):
    for i in prange(num_particles):
        densities[i] = calculate_density(positions[i, 0], positions[i, 1], 
                                      positions, boundary_particles, num_particles, bps)

@jit(nopython=True)
def calculate_gradient(point_x, point_y, predictedPositions, densities, boundary_particles, num_particles, bps, drag_pos, drag_vel):
    vector = np.zeros(2)
    
    # Reduced force multiplier for particle interactions
    particle_force = 5.0
    
    # Vectorized force calculation for normal particles
    for i in range(num_particles):
        diff = predictedPositions[i] - np.array([point_x, point_y])
        distance = np.sqrt(np.sum(diff**2))
        
        if distance > 0:
            dir_vector = diff / distance
            slope = smoothing_kernel_derivative(smoothing_radius, distance)
            vector += 80 * dir_vector * slope * particle_force / densities[i]
    
    # Reduced boundary force
    boundary_force = 500
    
    # Vectorized force calculation for boundary particles
    for i in range(4 * bps):
        diff = boundary_particles[i] - np.array([point_x, point_y])
        distance = np.sqrt(np.sum(diff**2))
        
        if distance > 0:
            dir_vector = diff / distance
            slope = smoothing_kernel_derivative(smoothing_radius, distance)
            vector += dir_vector * slope * boundary_force
    
    # Modified drag force with adjustable parameters
    drag_radius = 10  # Radius of influence for drag
    drag_strength = 280  # Base strength of drag force
    drag_velocity_influence = 1.4  # How much the drag velocity affects particles
    
    if drag_pos[0] >= 0:  # Check if drag is active
        diff = np.array([point_x, point_y]) - drag_pos
        distance = np.sqrt(np.sum(diff**2))
        if distance < drag_radius and distance > 0:
            dir_vector = diff / distance
            force_strength = (drag_radius - distance) / drag_radius * drag_strength
            vector += dir_vector * force_strength + drag_vel * drag_velocity_influence
    return vector

@jit(nopython=True)
def calculate_velocities(positions, velocities, predictedPositions, densities, boundary_particles, num_particles, bps, drag_pos, drag_vel):
    velocities *= velocity_damping
   
    for i in range(num_particles):
        force = calculate_gradient(positions[i, 0], positions[i, 1], 
                                 predictedPositions, densities, boundary_particles, 
                                 num_particles, bps, drag_pos, drag_vel) * 5
        
        # Add viscosity calculation
        viscosity_force = calculate_viscosity(positions[i, 0], positions[i, 1], 
                                            positions, velocities, num_particles)
        
        velocities[i] += force * 0.25 + viscosity_force * dt
        
        # Vectorized boundary collision checking with smoother response
        x_collision = (positions[i, 0] <= 0) | (positions[i, 0] >= N - 1)
        y_collision = (positions[i, 1] <= 0) | (positions[i, 1] >= N - 1)
        
        if x_collision:
            velocities[i, 0] *= -damping_factor
        if y_collision:
            velocities[i, 1] *= -damping_factor

# Create visualization
canvas = vispy.scene.SceneCanvas(keys='interactive', bgcolor='black', size=(700, 700))
view = canvas.central_widget.add_view()
view.camera = vispy.scene.PanZoomCamera(rect=(0, 0, 1, 1))
view.camera.flip = (False, True, False)
view.camera.set_range()

particle_visual = visuals.Markers()
boundary_visual = visuals.Markers()
view.add(particle_visual)
view.add(boundary_visual)

# Mouse handlers
@canvas.events.mouse_press.connect
def on_mouse_press(event):
    global drag_active, drag_start_pos, drag_current_pos
    if event.button == 1:  # Left click only
        pos = view.camera.transform.imap(event.pos)[:2]
        drag_start_pos = np.array([pos[0] * N, pos[1] * N])
        drag_current_pos = drag_start_pos.copy()
        drag_active = True

@canvas.events.mouse_move.connect
def on_mouse_move(event):
    global drag_current_pos, drag_velocity
    if drag_active:  # Only update if dragging
        pos = view.camera.transform.imap(event.pos)[:2]
        new_pos = np.array([pos[0] * N, pos[1] * N])
        drag_velocity = (new_pos - drag_current_pos) * 0.5
        drag_current_pos = new_pos

@canvas.events.mouse_release.connect
def on_mouse_release(event):
    global drag_active, drag_start_pos, drag_current_pos, drag_velocity
    if event.button == 1:
        drag_active = False
        drag_start_pos = np.array([-1, -1])
        drag_current_pos = np.array([-1, -1])
        drag_velocity = np.array([0., 0.])

# Update function
def update(event):
    global positions, velocities, predictedPositions, densities
    
    predictedPositions = positions + velocities * dt
    
    update_densities(positions, densities, boundary_particles, num_particles, bps)
    calculate_velocities(positions, velocities, predictedPositions, densities, 
                        boundary_particles, num_particles, bps, 
                        drag_current_pos, drag_velocity)
    
    positions += velocities * dt
    np.clip(positions, 0, N-1, out=positions)
    
    scaled_positions = positions / N
    speeds = np.linalg.norm(velocities, axis=1)
    colors = plt.get_cmap('plasma')(speeds / 1000)
    
    particle_visual.set_data(scaled_positions, edge_color='black', face_color=colors, size=12)

# Timer
timer = vispy.app.Timer(interval=0.016, connect=update, start=True)

canvas.show()
vispy.app.run()
