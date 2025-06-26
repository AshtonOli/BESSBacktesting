import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_nsw_energy_data(start_date, end_date, save_to_csv=True):
    """
    Generate realistic 5-minute NSW energy spot market data
    
    Parameters:
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format
    save_to_csv (bool): Whether to save data to CSV file
    
    Returns:
    pandas.DataFrame: Generated energy market data
    """
    
    # Convert string dates to datetime objects
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Generate 5-minute intervals
    date_range = pd.date_range(start=start, end=end, freq='5min')
    
    # Initialize data storage
    data = []
    
    # Base parameters for NSW energy market
    base_price = 45.0  # Base price in AUD/MWh
    seasonal_multiplier = 1.0
    
    for timestamp in date_range:
        # Extract time components
        hour = timestamp.hour
        day_of_week = timestamp.weekday()  # 0 = Monday, 6 = Sunday
        month = timestamp.month
        
        # Seasonal adjustments
        if month in [12, 1, 2]:  # Summer - higher demand due to cooling
            seasonal_multiplier = 1.4
        elif month in [6, 7, 8]:  # Winter - higher demand due to heating
            seasonal_multiplier = 1.2
        else:  # Spring/Autumn
            seasonal_multiplier = 1.0
        
        # Daily demand pattern
        if 6 <= hour <= 9:  # Morning peak
            demand_multiplier = 1.6
        elif 17 <= hour <= 20:  # Evening peak
            demand_multiplier = 1.8
        elif 22 <= hour or hour <= 5:  # Overnight low demand
            demand_multiplier = 0.6
        else:  # Standard daytime
            demand_multiplier = 1.0
        
        # Weekend adjustment (lower commercial demand)
        if day_of_week >= 5:  # Weekend
            demand_multiplier *= 0.8
        
        # Calculate base spot price
        spot_price = base_price * seasonal_multiplier * demand_multiplier
        
        # Add random volatility and occasional price spikes
        volatility = np.random.normal(0, 0.15)  # 15% standard volatility
        spot_price *= (1 + volatility)
        
        # Occasional price spikes (1% chance) - can reach market price cap
        if random.random() < 0.01:
            # Extreme price events can reach very high levels
            if random.random() < 0.1:  # 10% of spikes are extreme (reaching towards cap)
                spot_price = random.uniform(5000, 15000)
            else:
                spike_multiplier = random.uniform(3, 8)
                spot_price *= spike_multiplier
        
        # Check for negative pricing conditions
        # This occurs when renewable generation significantly exceeds demand
        
        
        
        
        # Generate demand (MW) - correlated with price patterns
        base_demand = 8000  # Base demand in MW
        demand = base_demand * demand_multiplier * seasonal_multiplier
        demand += np.random.normal(0, 200)  # Add some noise
        demand = max(demand, 4000)  # Minimum demand
        
        # Generate renewable generation (wind + solar)
        solar_generation = 0
        if 6 <= hour <= 18:  # Solar only during daylight
            max_solar = 2500  # Maximum solar capacity
            solar_efficiency = (np.sin((hour - 6) * np.pi / 12) ** 2) * np.random.uniform(0.7, 1.0)
            solar_generation = max_solar * solar_efficiency
        
        # Wind generation (random but somewhat consistent)
        wind_generation = np.random.uniform(500, 3000)
        
        # Total renewable generation
        renewable_generation = solar_generation + wind_generation
        
        # Calculate renewable percentage
        renewable_percentage = (renewable_generation / demand) * 100
        
        # Network losses (typically 5-10%)
        network_losses = demand * np.random.uniform(0.05, 0.10)

        oversupply_ratio = renewable_generation / demand
        
        if oversupply_ratio > 0.8:  # High renewable penetration
            # Chance of negative pricing increases with oversupply
            negative_price_chance = min((oversupply_ratio - 0.8) * 0.5, 0.15)  # Max 15% chance
            
            if random.random() < negative_price_chance:
                # Generate negative price - can go to market floor
                if random.random() < 0.05:  # 5% chance of extreme negative pricing
                    spot_price = random.uniform(-16000, -1000)  # Extreme negative events
                else:
                    spot_price = random.uniform(-200, -5)  # Typical negative pricing
        # Apply NEM market price caps: floor of -$16,000/MWh, ceiling of +$16,600/MWh
        spot_price = max(min(spot_price, 16600), -16000)
        # Append data point
        data.append({
            'timestamp': timestamp,
            'spot_price_aud_mwh': round(spot_price, 2),
            'demand_mw': round(demand, 1),
            'solar_generation_mw': round(solar_generation, 1),
            'wind_generation_mw': round(wind_generation, 1),
            'renewable_generation_mw': round(renewable_generation, 1),
            'renewable_percentage': round(renewable_percentage, 1),
            'network_losses_mw': round(network_losses, 1),
            'trading_interval': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV if requested
    if save_to_csv:
        filename = f'nsw_energy_data_{start_date}_to_{end_date}.csv'
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    
    return df

def display_summary_stats(df):
    """Display summary statistics for the generated data"""
    print("\n=== NSW Energy Market Data Summary ===")
    print(f"Data period: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"Total intervals: {len(df)}")
    print(f"\nSpot Price Statistics (AUD/MWh):")
    print(f"  Mean: ${df['spot_price_aud_mwh'].mean():.2f}")
    print(f"  Median: ${df['spot_price_aud_mwh'].median():.2f}")
    print(f"  Min: ${df['spot_price_aud_mwh'].min():.2f}")
    print(f"  Max: ${df['spot_price_aud_mwh'].max():.2f}")
    print(f"  Std Dev: ${df['spot_price_aud_mwh'].std():.2f}")
    print(f"\nDemand Statistics (MW):")
    print(f"  Mean: {df['demand_mw'].mean():.1f} MW")
    print(f"  Peak: {df['demand_mw'].max():.1f} MW")
    print(f"  Minimum: {df['demand_mw'].min():.1f} MW")
    print(f"\nRenewable Generation:")
    print(f"  Average renewable percentage: {df['renewable_percentage'].mean():.1f}%")
    print(f"  Max renewable percentage: {df['renewable_percentage'].max():.1f}%\n")

# Example usage
if __name__ == "__main__":
    # Generate data for the last 30 days
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    print(f"Generating NSW energy market data from {start_date} to {end_date}")
    
    # Generate the data
    energy_data = generate_nsw_energy_data(start_date, end_date)
    
    # Display summary statistics
    display_summary_stats(energy_data)
    
    # Show first few rows
    print("\n=== Sample Data (First 10 rows) ===")
    print(energy_data.head(10).to_string(index=False))
    
    print(f"\n✅ Generated {len(energy_data)} data points with 5-minute intervals")
    print("📊 Data includes realistic pricing patterns, demand cycles, and renewable generation")
    print("💾 Data saved to CSV file for further analysis")