import numpy as np
import matplotlib.pyplot as plt

# Replace this with your actual simulation data
# For example:
# space = np.load('simulation_results.npy')
# For demonstration, let's create a synthetic version similar to yours
def create_synthetic_data(length, transition_point=5000, residual=0.0001):
    # This function simulates your observed behavior
    r = np.arange(1, length + 1)
    # The pure inverse quadratic law
    inverse_sq_part = 1.0 / r**2
    
    # Create a smooth transition
    transition_start = int(transition_point * 0.9)
    transition_end = int(transition_point * 1.1)
    
    # Brachistochrone-like behavior at small distances (represented as an enhanced decay)
    small_dist_part = 1.0 / r**3
    
    # Combine the different behaviors
    space_data = np.zeros(length)
    space_data[:transition_start] = small_dist_part[:transition_start]
    space_data[transition_end:] = inverse_sq_part[transition_end:]
    
    # Smooth the transition area
    for i in range(transition_start, transition_end):
        alpha = (i - transition_start) / (transition_end - transition_start)
        space_data[i] = (1 - alpha) * small_dist_part[i] + alpha * inverse_sq_part[i]

    # Add the non-decreasing residual
    space_data += residual
    
    # Normalize to get a probability distribution and then scale to simulate particle counts
    space_data /= np.sum(space_data)
    total_particles = 1000000
    return np.round(space_data * total_particles).astype(int)

# Use the function to get your simulation's particle count data
'''
space = create_synthetic_data(10000)

print(f"Shape of the input data: {space.shape}")
print(f"Total number of particles: {np.sum(space)}")
'''

def compute_power_spectrum(space):
    # Number of data points
    n = len(space)

    # Sample spacing is 1, as each element represents a single position 'i'
    d = 1.0 

    # Compute the FFT
    fft_result = np.fft.fft(space)

    # Compute the frequencies (wavenumbers)
    frequencies = np.fft.fftfreq(n, d=d)

    # Calculate the power spectrum
    power_spectrum = np.abs(fft_result)**2

    # Isolate positive frequencies and corresponding power (for a real signal, the spectrum is symmetric)
    positive_frequencies_mask = frequencies > 0
    positive_frequencies = frequencies[positive_frequencies_mask]
    positive_power = power_spectrum[positive_frequencies_mask]

    # Sort the frequencies for correct plotting
    sort_indices = np.argsort(positive_frequencies)
    positive_frequencies = positive_frequencies[sort_indices]
    positive_power = positive_power[sort_indices]

    return positive_frequencies, positive_power

def plot_power_spectrum(positive_frequencies, positive_power):
    # Plot the power spectrum on a log-log scale
    plt.figure(figsize=(10, 6))
    plt.loglog(positive_frequencies, positive_power, label='Power Spectrum')
    plt.xlabel('Frequency (1/space units)')
    plt.ylabel('Power')
    plt.title('Power Spectrum of Particle Distribution')

    # Fit a line to the mesoscopic region to find the slope
    # Define a frequency range to fit, avoiding the low-frequency residual spike and high-frequency noise
    # These frequency limits correspond to your mesoscopic scale.
    low_freq_cut = 4e-3  # Low frequency limit to avoid residual spike
    high_freq_cut = 0.4  # Arbitrary limit to avoid high-frequency noise

    freq_range_mask = (positive_frequencies > low_freq_cut) & (positive_frequencies < high_freq_cut)
    freqs_to_fit = positive_frequencies[freq_range_mask]
    power_to_fit = positive_power[freq_range_mask]

    # Perform the linear fit on the log-log data
    coeffs = np.polyfit(np.log(freqs_to_fit), np.log(power_to_fit), 1)
    spectral_slope = coeffs[0]

    # Plot the fitted line
    plt.loglog(freqs_to_fit, np.exp(np.polyval(coeffs, np.log(freqs_to_fit))),
            '--', color='red', label=f'Fit: slope={spectral_slope:.2f}')

    # Label the zero-frequency spike, which corresponds to your residual distribution
    # The lowest frequency component
    plt.text(positive_frequencies[0], positive_power[0], '  (Residual)', verticalalignment='top')

    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.show()

    print(f"The spectral slope in the mesoscopic range is approximately: {spectral_slope:.2f}")

def analyze_spectrum(space):
    positive_frequencies, positive_power = compute_power_spectrum(space)
    plot_power_spectrum(positive_frequencies, positive_power)   
    
    