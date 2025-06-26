from synthetic_data.gen_synethic_spot_data import generate_nsw_energy_data,display_summary_stats
import datetime as dt
from src.battery import Battery
from src.util import parse_json,dollar_format
from src.visualise import display_data

def main() -> None:
    #Parse config & params
    config = parse_json("config.json")
    battery_params = config["battery"]

    #Generate synthetic data
    end_date = dt.datetime.now()
    start_date = end_date - dt.timedelta(days = 90)
    df = generate_nsw_energy_data(start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d'),False)
    display_summary_stats(df)

    #Instantiate battery
    bess = Battery(battery_params["name"],battery_params["capacity"],battery_params["charge_rate"],battery_params["dispatch_rate"])
    print(bess)

    for i,row in df.iterrows():
        df.loc[i,bess.name + "_dispatch"] = bess.logic(row)
        df.loc[i,bess.name + "_cost"] = row.spot_price_aud_mwh * df.loc[i,bess.name + "_dispatch"]
        df.loc[i,bess.name + "_capacity"] = bess.current_capacity
    
    print("======= Analysis =========")
    print(f"Total money made by battery: {dollar_format(df[bess.name + '_cost'].sum())}")
    print(f"Average energy of {bess.name} : {df[bess.name + '_capacity'].mean()} MW")

    display_data(df)

if __name__ == '__main__':
    main()