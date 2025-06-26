import pandas as pd
import datetime as dt
class Battery:
    def __init__(self, name, capacity, charge_rate,dispatch_rate) -> None:
        self.name = name
        self.capacity = capacity
        self.charge_rate = charge_rate
        self.dispatch_rate = dispatch_rate
        self.current_capacity = 0

    def __str__(self):
        return f"""{self.name}
Capacity: {self.capacity} MWh
Charge Rate: {self.charge_rate} MW
Dispatch Rate: {self.dispatch_rate} MW
Current Charge: {self.current_capacity} MW
"""

    def charge(self,mw):
        if self.current_capacity + mw > self.capacity:
            # print(f"Cannot charge that much, only {self.capacity - self.current_capacity}")
            charged = self.capacity - self.current_capacity
        else:
            charged= mw
        self.current_capacity += charged
        return charged
    
    def dispatch(self,mw):
        if self.current_capacity - mw < 0:
            # print(f"Cannot dispatch that much, only {self.current_capacity}")
            dispatched = self.current_capacity
        else:    
            dispatched= mw
        self.current_capacity -= dispatched
        return dispatched
    
    def logic(self,row : pd.Series):
        if row.timestamp.time() >= dt.time(11,0,0) and row.timestamp.time() <= dt.time(14,0,0):
            mw = -self.charge(self.charge_rate/20)
        elif row.timestamp.time() >= dt.time(17,0,0) and row.timestamp.time() <= dt.time(19,0,0):
            mw = self.dispatch(self.dispatch_rate/20)
        else:
            mw = 0

        return mw
            
    
        

    