import numpy as np
from datetime import datetime

class CompostState:
    def __init__(self, initial_mass_kg=20.0, initial_cn=30.0):
        # Constants for Composition (approximate based on food waste/chips mix)
        self.initial_mass = initial_mass_kg
        self.carbon_fraction = 0.50 * 0.40 # 50% dry matter, of which 40% is Carbon
        self.nitrogen_fraction = self.carbon_fraction / initial_cn
        
        # State Variables (Mass in kg)
        self.mass_C = initial_mass_kg * self.carbon_fraction
        self.mass_N = initial_mass_kg * self.nitrogen_fraction
        
        self.last_update = datetime.utcnow()
        
        # Physics Constants
        # PTFE membrane limits flow, but heat drives it.
        # Base flow (diffusion) + Convective flow (Temp delta)
        self.BASE_FLOW_M3H = 0.05 # 50L/h (diffusion estimate)
        self.CONVECTION_COEFF = 0.01 # m3/h per degree delta T
        
        # Gas Constants (kg/m3 at STP approximation)
        self.DENSITY_CO2 = 1.98 
        self.DENSITY_NH3 = 0.77
        self.DENSITY_CH4 = 0.72

    def estimate_airflow(self, temp_compost, temp_air):
        """
        Estimates airflow through PTFE membrane driven by thermal convection.
        Q_air = Base_Diffusion + k * sqrt(T_compost - T_air)
        Natural convection follows a power law (or sqrt), not linear.
        """
        delta_t = max(0, temp_compost - temp_air)
        # Sqrt better modles natural convection (chimney effect)
        # Coeff adapted to keep roughly same magnitude at dt=40 (~6.3 * 0.01 = 0.06)
        # Old linear: 0.05 + 0.01 * 40 = 0.45 m3/h
        # New sqrt: 0.05 + 0.06 * 6.3 = 0.43 m3/h
        CONV_COEFF_SQRT = 0.06 
        return self.BASE_FLOW_M3H + (CONV_COEFF_SQRT * np.sqrt(delta_t))

    def update(self, current_time, measures, temp_air=20.0):
        """
        Updates the mass balance based on sensor readings and estimated airflow.
        measures: dict with keys 'co2' (ppm), 'mq137' (raw ADC), 'mq4' (raw ADC), 'temp_scd'
        """
        dt_seconds = (current_time - self.last_update).total_seconds()
        dt_hours = dt_seconds / 3600.0
        
        if dt_hours <= 0:
            return self.get_cn()
            
        # 1. Estimate Flow
        q_air = self.estimate_airflow(measures.get('temp_scd', 20), temp_air)
        
        # 2. Gas Concentrations (CRITICAL: Convert ADC to pseudo-PPM)
        # Default scaling: 1/10 roughly maps 2000 ADC -> 200 PPM.
        # This is temporary until real calibration (Rs/Ro).
        co2_vol = measures.get('co2', 400) * 1e-6
        
        mq137_raw = measures.get('mq137', 0)
        nh3_ppm = mq137_raw * 0.1 # <--- CALIBRATION STUB
        nh3_vol = nh3_ppm * 1e-6 
        
        mq4_raw = measures.get('mq4', 0)
        ch4_ppm = mq4_raw * 0.1 # <--- CALIBRATION STUB
        ch4_vol = ch4_ppm * 1e-6
        
        # 3. Calculate Mass Fluxes (kg/h)
        # Flux = Q_air * Concentration * Density * (MolarMassRatio C or N)
        
        # Carbon Flux (CO2 + CH4)
        flux_c_co2 = q_air * co2_vol * self.DENSITY_CO2 * (12/44)
        flux_c_ch4 = q_air * ch4_vol * self.DENSITY_CH4 * (12/16)
        total_c_loss = (flux_c_co2 + flux_c_ch4) * dt_hours
        
        # Nitrogen Flux (NH3)
        flux_n_nh3 = q_air * nh3_vol * self.DENSITY_NH3 * (14/17)
        total_n_loss = flux_n_nh3 * dt_hours
        
        # 4. Update State
        self.mass_C = max(0, self.mass_C - total_c_loss)
        self.mass_N = max(0, self.mass_N - total_n_loss)
        
        self.last_update = current_time
        
        return self.get_cn(), q_air

    def get_cn(self):
        if self.mass_N == 0: return 999.0
        return self.mass_C / self.mass_N

# Test Integration
if __name__ == "__main__":
    compost = CompostState(initial_mass_kg=100.0, initial_cn=30.0)
    print(f"Initial C/N: {compost.get_cn():.2f}")
    
    # Simulate 24h of active composting (Thermophilic 60C)
    # High CO2 (3000ppm), Some NH3 (ADC 100 -> ~10ppm)
    for _ in range(24):
        now = datetime.utcnow() # Note: In real sim we'd increment time
        # Mocking time step as 1 hour manually in logic for test
        compost.last_update = datetime.fromtimestamp(compost.last_update.timestamp() - 3600) 
        
        cn, flow = compost.update(now, {
            'temp_scd': 60,
            'co2': 3000,
            'mq137': 100, # NH3 (Raw ADC)
            'mq4': 0
        }, temp_air=15)
        
    print(f"Final C/N (24h later): {cn:.4f}")
    print(f"Est. Airflow: {flow:.4f} m3/h")
